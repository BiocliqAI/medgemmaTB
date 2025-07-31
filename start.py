#!/usr/bin/env python3
"""
Railway startup script for MedGemma TB Detector
"""

import os
import sys

# Add backend directory to Python path
sys.path.insert(0, '/app/backend')

# Set working directory
os.environ['PYTHONPATH'] = '/app/backend:/app'

if __name__ == "__main__":
    try:
        # Import from backend directory
        sys.path.insert(0, '/app/backend')
        from main import app
        import uvicorn
        
        # Get port from Railway environment  
        port = int(os.environ.get("PORT", 8000))
        
        print(f"🚀 Starting on 0.0.0.0:{port}")
        print(f"🔑 HF Token: {bool(os.environ.get('HUGGINGFACE_API_TOKEN'))}")
        
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)