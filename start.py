#!/usr/bin/env python3
"""
Startup script for the STL Weight Estimator API
This script provides an easy way to start the development server
"""

import uvicorn
import sys
import os

def main():
    """Start the FastAPI development server"""
    
    # Default configuration
    host = "0.0.0.0"
    port = 8000
    reload = True
    
    # Check for environment variables
    if os.getenv("PORT"):
        port = int(os.getenv("PORT"))
    
    if os.getenv("HOST"):
        host = os.getenv("HOST")
    
    if os.getenv("ENVIRONMENT") == "production":
        reload = False
    
    print(f"🚀 Starting STL Weight Estimator API...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🏥 Health Check: http://{host}:{port}/health")
    print(f"🧪 Test Page: http://{host}:{port}/test.html")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 