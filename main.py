from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
import numpy as np
import trimesh
import tempfile
import os
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="STL Weight Estimator API",
    description="A lightweight API to estimate the weight of 3D printed objects from STL files",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

class PrintingParameters(BaseModel):
    infill_percentage: float = Field(..., ge=0, le=100, description="Infill percentage (0-100)")
    material_density: float = Field(..., gt=0, description="Material density in g/cm³")
    line_thickness: float = Field(..., gt=0, description="Line thickness in mm")
    layer_height: Optional[float] = Field(None, gt=0, description="Layer height in mm (optional)")
    shell_count: Optional[int] = Field(None, ge=1, description="Number of shells (optional)")

    @validator('infill_percentage')
    def validate_infill(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Infill percentage must be between 0 and 100')
        return v

    @validator('material_density')
    def validate_density(cls, v):
        if v <= 0:
            raise ValueError('Material density must be positive')
        return v

    @validator('line_thickness')
    def validate_thickness(cls, v):
        if v <= 0:
            raise ValueError('Line thickness must be positive')
        return v

class WeightEstimateResponse(BaseModel):
    weight_grams: float
    total_volume_cm3: float
    solid_volume_cm3: float
    infill_volume_cm3: float
    shell_volume_cm3: float

def calculate_stl_volume(stl_file_path: str) -> float:
    """
    Calculate the volume of an STL file in cubic centimeters
    """
    try:
        # Load the mesh using trimesh
        mesh = trimesh.load(stl_file_path)
        
        # Check if mesh is valid
        if not mesh.is_valid:
            raise ValueError("Invalid mesh geometry")
        
        # Calculate volume in cubic millimeters and convert to cubic centimeters
        volume_mm3 = mesh.volume
        volume_cm3 = volume_mm3 / 1000  # Convert mm³ to cm³
        
        logger.info(f"Calculated volume: {volume_cm3:.4f} cm³")
        return volume_cm3
    
    except Exception as e:
        logger.error(f"Error calculating STL volume: {str(e)}")
        raise ValueError(f"Failed to process STL file: {str(e)}")

def estimate_printing_volume(
    total_volume_cm3: float,
    infill_percentage: float,
    line_thickness_mm: float,
    layer_height_mm: Optional[float] = None,
    shell_count: Optional[int] = None
) -> tuple[float, float, float]:
    """
    Estimate the actual printing volume considering infill and shells
    Returns: (solid_volume, infill_volume, shell_volume)
    """
    # Default values
    if layer_height_mm is None:
        layer_height_mm = 0.2  # Default layer height
    
    if shell_count is None:
        shell_count = 2  # Default shell count
    
    # Convert to cm for calculations
    line_thickness_cm = line_thickness_mm / 10
    layer_height_cm = layer_height_mm / 10
    
    # Estimate shell thickness (typically 2-3 line widths)
    shell_thickness_cm = line_thickness_cm * 2.5
    
    # Calculate shell volume (outer surface area * shell thickness)
    # This is a simplified calculation - in reality, it's more complex
    surface_area_cm2 = (total_volume_cm3 ** (2/3)) * 6  # Approximate surface area
    shell_volume_cm3 = surface_area_cm2 * shell_thickness_cm * shell_count
    
    # Calculate infill volume (remaining volume * infill percentage)
    remaining_volume_cm3 = total_volume_cm3 - shell_volume_cm3
    infill_volume_cm3 = remaining_volume_cm3 * (infill_percentage / 100)
    
    # Solid volume is shell + infill
    solid_volume_cm3 = shell_volume_cm3 + infill_volume_cm3
    
    logger.info(f"Volume breakdown - Total: {total_volume_cm3:.4f}, "
                f"Shell: {shell_volume_cm3:.4f}, Infill: {infill_volume_cm3:.4f}, "
                f"Solid: {solid_volume_cm3:.4f} cm³")
    
    return solid_volume_cm3, infill_volume_cm3, shell_volume_cm3

@app.post("/estimate-weight", response_model=WeightEstimateResponse)
async def estimate_weight(
    file: UploadFile = File(..., description="STL file to analyze"),
    infill_percentage: float = Form(..., ge=0, le=100, description="Infill percentage (0-100)"),
    material_density: float = Form(..., gt=0, description="Material density in g/cm³"),
    line_thickness: float = Form(..., gt=0, description="Line thickness in mm"),
    layer_height: Optional[float] = Form(None, gt=0, description="Layer height in mm (optional)"),
    shell_count: Optional[int] = Form(None, ge=1, description="Number of shells (optional)")
):
    """
    Estimate the weight of a 3D printed object from an STL file
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.stl'):
            raise HTTPException(status_code=400, detail="File must be an STL file")
        
        # Create temporary file to process STL
        with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as temp_file:
            # Write uploaded file to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Calculate total volume
            total_volume_cm3 = calculate_stl_volume(temp_file_path)
            
            # Estimate printing volumes
            solid_volume_cm3, infill_volume_cm3, shell_volume_cm3 = estimate_printing_volume(
                total_volume_cm3=total_volume_cm3,
                infill_percentage=infill_percentage,
                line_thickness_mm=line_thickness,
                layer_height_mm=layer_height,
                shell_count=shell_count
            )
            
            # Calculate weight
            weight_grams = solid_volume_cm3 * material_density
            
            logger.info(f"Weight estimation complete: {weight_grams:.2f} grams")
            
            return WeightEstimateResponse(
                weight_grams=round(weight_grams, 2),
                total_volume_cm3=round(total_volume_cm3, 4),
                solid_volume_cm3=round(solid_volume_cm3, 4),
                infill_volume_cm3=round(infill_volume_cm3, 4),
                shell_volume_cm3=round(shell_volume_cm3, 4)
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "STL Weight Estimator API",
        "version": "1.0.0",
        "endpoints": {
            "estimate_weight": "POST /estimate-weight",
            "docs": "GET /docs",
            "test_page": "GET /test"
        }
    }

@app.get("/test", response_class=HTMLResponse)
async def test_page():
    """
    Serve the test HTML page
    """
    try:
        with open("test.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Test page not found</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 