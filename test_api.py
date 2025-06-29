#!/usr/bin/env python3
"""
Test script for the STL Weight Estimator API
This script creates a simple test STL file and tests the API endpoints
"""

import requests
import tempfile
import os
import numpy as np
from stl import mesh

def create_test_stl():
    """
    Create a simple cube STL file for testing
    """
    # Create a simple cube
    vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ])
    
    # Define the faces of the cube
    faces = np.array([
        [0, 3, 1],
        [1, 3, 2],
        [0, 4, 7],
        [0, 7, 3],
        [4, 5, 6],
        [4, 6, 7],
        [5, 1, 2],
        [5, 2, 6],
        [2, 3, 6],
        [3, 7, 6],
        [0, 1, 5],
        [0, 5, 4]
    ])
    
    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j]]
    
    return cube

def test_api():
    """
    Test the API endpoints
    """
    base_url = "http://localhost:8000"
    
    print("Testing STL Weight Estimator API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running on localhost:8000")
        return
    
    # Test root endpoint
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
    
    # Create test STL file
    print("\n3. Creating test STL file...")
    cube = create_test_stl()
    
    with tempfile.NamedTemporaryFile(suffix='.stl', delete=False) as temp_file:
        cube.save(temp_file.name)
        temp_file_path = temp_file.name
    
    try:
        # Test weight estimation endpoint
        print("\n4. Testing weight estimation endpoint...")
        
        with open(temp_file_path, 'rb') as stl_file:
            files = {'file': ('test_cube.stl', stl_file, 'application/octet-stream')}
            data = {
                'infill_percentage': 20,
                'material_density': 1.24,  # PLA
                'line_thickness': 0.4,
                'layer_height': 0.2,
                'shell_count': 2
            }
            
            response = requests.post(f"{base_url}/estimate-weight", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Weight estimation successful!")
                print(f"   Weight: {result['weight_grams']} grams")
                print(f"   Total Volume: {result['total_volume_cm3']} cm³")
                print(f"   Solid Volume: {result['solid_volume_cm3']} cm³")
                print(f"   Infill Volume: {result['infill_volume_cm3']} cm³")
                print(f"   Shell Volume: {result['shell_volume_cm3']} cm³")
            else:
                print(f"❌ Weight estimation failed: {response.status_code}")
                print(f"   Error: {response.text}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
    
    # Test error handling
    print("\n5. Testing error handling...")
    
    # Test with invalid file type
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
        temp_file.write(b"This is not an STL file")
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as txt_file:
            files = {'file': ('test.txt', txt_file, 'text/plain')}
            data = {
                'infill_percentage': 20,
                'material_density': 1.24,
                'line_thickness': 0.4
            }
            
            response = requests.post(f"{base_url}/estimate-weight", files=files, data=data)
            print(f"Invalid file test: {response.status_code} - {response.json()}")
    
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
    
    print("\n✅ API testing completed!")

if __name__ == "__main__":
    test_api() 