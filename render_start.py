#!/usr/bin/env python3
"""
Production startup script for Render deployment
This script is optimized for production environments
"""

import uvicorn
import os

def main():
    """Start the FastAPI production server"""
    
    # Get port from environment variable (Render sets this)
    port = int(os.getenv("PORT", 8000))
    
    # Use 0.0.0.0 to bind to all available network interfaces
    host = "0.0.0.0"
    
    print(f"🚀 Starting STL Weight Estimator API in production mode...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🌐 Environment: Production")
    print("=" * 50)
    
    # Start the server without reload for production
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # No reload in production
        log_level="info"
    )

if __name__ == "__main__":
    main() 