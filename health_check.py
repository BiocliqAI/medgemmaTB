#!/usr/bin/env python3
"""
Simple health check server for Railway debugging
"""

from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Health check server running"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "tb-detector",
        "environment": "railway",
        "port": os.environ.get("PORT", "8000"),
        "hf_token_configured": bool(os.environ.get("HUGGINGFACE_API_TOKEN"))
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🔍 Health check server starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)