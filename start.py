#!/usr/bin/env python3
"""
Railway startup script for MedGemma TB Detector
"""

import os
import sys
import time

def main():
    print("=" * 50)
    print("🚀 MedGemma TB Detector - Railway Startup")
    print("=" * 50)
    
    # Debug environment
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path}")
    print(f"🔑 HF Token present: {bool(os.environ.get('HUGGINGFACE_API_TOKEN'))}")
    print(f"🌐 PORT env: {os.environ.get('PORT', 'Not set')}")
    
    # List directory contents
    print(f"📋 App directory contents: {os.listdir('/app')}")
    if os.path.exists('/app/backend'):
        print(f"📋 Backend directory contents: {os.listdir('/app/backend')}")
    
    try:
        # Add paths
        sys.path.insert(0, '/app')
        sys.path.insert(0, '/app/backend')
        
        print("📦 Importing dependencies...")
        
        # Test imports one by one
        print("  - Importing FastAPI...")
        from fastapi import FastAPI
        
        print("  - Importing uvicorn...")
        import uvicorn
        
        print("  - Importing main application...")
        
        # Try to import the main app
        try:
            from main import app
            print("  ✅ Main app imported successfully")
        except ImportError as e:
            print(f"  ❌ Failed to import main app: {e}")
            # Try alternative import
            import main
            app = main.app
            print("  ✅ Main app imported via alternative method")
        
        # Get port
        port = int(os.environ.get("PORT", 8000))
        print(f"🌐 Starting server on 0.0.0.0:{port}")
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Wait a bit before exiting to see logs
        print("⏱️ Waiting 10 seconds before exit...")
        time.sleep(10)
        sys.exit(1)

if __name__ == "__main__":
    main()