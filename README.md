# STL Weight Estimator API

A production-ready REST API built with FastAPI that estimates the weight of 3D printed objects from STL files. The API calculates the total volume of the mesh and estimates the actual printing volume based on infill percentage, shell count, and other printing parameters.

## Features

- **STL File Processing**: Parse and analyze 3D STL files using trimesh
- **Volume Calculation**: Calculate total solid volume of the mesh
- **Printing Parameter Estimation**: Consider infill percentage, shell count, and line thickness
- **Weight Calculation**: Multiply estimated volume by material density
- **Comprehensive Error Handling**: Validate files and parameter ranges
- **RESTful API**: Clean, documented endpoints with automatic OpenAPI docs
- **Production Ready**: Deployed and accessible via HTTPS

## API Endpoints

### POST /estimate-weight

Estimates the weight of a 3D printed object from an STL file.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Parameters:**
  - `file` (required): STL file to analyze
  - `infill_percentage` (required): Infill percentage (0-100)
  - `material_density` (required): Material density in g/cm³
  - `line_thickness` (required): Line thickness in mm
  - `layer_height` (optional): Layer height in mm (default: 0.2)
  - `shell_count` (optional): Number of shells (default: 2)

**Response:**
```json
{
  "weight_grams": 27.45,
  "total_volume_cm3": 15.2345,
  "solid_volume_cm3": 12.1234,
  "infill_volume_cm3": 8.5678,
  "shell_volume_cm3": 3.5556
}
```

### GET /

Returns API information and available endpoints.

### GET /health

Health check endpoint for monitoring.

### GET /docs

Interactive API documentation (Swagger UI).

### GET /test

Web interface for testing the API.

## Live API

**Production URL**: https://stl-api-66l8.onrender.com

- **API Documentation**: https://stl-api-66l8.onrender.com/docs
- **Test Interface**: https://stl-api-66l8.onrender.com/test
- **Health Check**: https://stl-api-66l8.onrender.com/health

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd stl-weight-estimator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python render_start.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t stl-weight-estimator .
```

2. Run the container:
```bash
docker run -p 8000:8000 stl-weight-estimator
```

## Usage Examples

### Using curl

```bash
curl -X POST "https://stl-api-66l8.onrender.com/estimate-weight" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@model.stl" \
  -F "infill_percentage=20" \
  -F "material_density=1.24" \
  -F "line_thickness=0.4" \
  -F "layer_height=0.2" \
  -F "shell_count=3"
```

### Using Python requests

```python
import requests

url = "https://stl-api-66l8.onrender.com/estimate-weight"
files = {"file": open("model.stl", "rb")}
data = {
    "infill_percentage": 20,
    "material_density": 1.24,
    "line_thickness": 0.4,
    "layer_height": 0.2,
    "shell_count": 3
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(f"Weight: {result['weight_grams']} grams")
```

### Using JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('infill_percentage', '20');
formData.append('material_density', '1.24');
formData.append('line_thickness', '0.4');
formData.append('layer_height', '0.2');
formData.append('shell_count', '3');

fetch('https://stl-api-66l8.onrender.com/estimate-weight', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(`Weight: ${data.weight_grams} grams`));
```

## Common Material Densities

| Material | Density (g/cm³) |
|----------|-----------------|
| PLA | 1.24 |
| ABS | 1.04 |
| PETG | 1.27 |
| TPU | 1.20 |
| Nylon | 1.13 |
| Polycarbonate | 1.20 |

## Error Handling

The API includes comprehensive error handling for:

- Invalid file types (non-STL files)
- Corrupted or invalid STL files
- Parameter validation (out-of-range values)
- Processing errors
- Server errors

All errors return appropriate HTTP status codes and descriptive error messages.

## Technical Details

- **Framework**: FastAPI
- **STL Processing**: trimesh library
- **Volume Calculation**: Mesh volume calculation with unit conversion
- **Printing Estimation**: Simplified model considering shells and infill
- **File Handling**: Temporary file processing with automatic cleanup
- **Deployment**: Render (free tier)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 