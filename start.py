#!/usr/bin/env python3
"""
Railway startup script for MedGemma TB Detector
Starts the FastAPI server with proper configuration
"""

import os
import sys
import subprocess

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

# Import and run the main application
if __name__ == "__main__":
    try:
        from main import app
        import uvicorn
        
        # Get port from environment (Railway sets this)
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        
        print(f"🚀 Starting MedGemma TB Detector on {host}:{port}")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🔑 HF API Token configured: {bool(os.environ.get('HUGGINGFACE_API_TOKEN'))}")
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)