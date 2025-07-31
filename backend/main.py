from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

from models.medgemma_model import MedGemmaModel
from services.image_processor import ImageProcessor
from services.tb_analyzer import TBAnalyzer

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="TB Detector API",
    description="Chest X-ray Tuberculosis Detection using MedGemma-4B",
    version="1.0.0"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
image_processor = ImageProcessor()
tb_analyzer = TBAnalyzer()

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = MedGemmaModel()
        await model.load_model()
        print("✅ MedGemma-4B API connection established successfully")
    except Exception as e:
        print(f"❌ Failed to establish API connection: {e}")
        print("💡 Make sure to set HUGGINGFACE_API_TOKEN environment variable")
        # Don't raise the exception to allow the server to start
        # The health endpoint will indicate the model status

@app.get("/")
async def root():
    return {"message": "TB Detector API", "status": "running"}

@app.get("/health")
async def health_check():
    model_status = "connected" if model and model.is_loaded else "not_connected"
    has_api_token = bool(os.getenv("HUGGINGFACE_API_TOKEN"))
    
    return {
        "status": "healthy",
        "model_status": model_status,
        "api_version": "1.0.0",
        "deployment": "huggingface_api",
        "has_api_token": has_api_token,
        "model_info": model.get_model_info() if model else None
    }

@app.post("/analyze")
async def analyze_xray(file: UploadFile = File(...)):
    if not model or not model.is_loaded:
        raise HTTPException(
            status_code=503, 
            detail="API connection not established. Please check HUGGINGFACE_API_TOKEN environment variable."
        )
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            processed_image = image_processor.preprocess_image(tmp_file_path)
            
            result = await model.analyze_image(processed_image)
            
            tb_analysis = tb_analyzer.analyze_for_tb(result)
            
            return JSONResponse({
                "success": True,
                "filename": file.filename,
                "analysis": {
                    "raw_report": result,
                    "tb_analysis": tb_analysis,
                    "confidence": tb_analysis.get("confidence", 0.0),
                    "findings": tb_analysis.get("findings", []),
                    "recommendation": tb_analysis.get("recommendation", "")
                },
                "disclaimer": "This analysis is for research purposes only and should not be used for medical diagnosis."
            })
            
        finally:
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/batch-analyze")
async def batch_analyze(files: list[UploadFile] = File(...)):
    if not model or not model.is_loaded:
        raise HTTPException(
            status_code=503, 
            detail="API connection not established. Please check HUGGINGFACE_API_TOKEN environment variable."
        )
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
    
    results = []
    
    for file in files:
        if not file.content_type.startswith("image/"):
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "File must be an image"
            })
            continue
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                processed_image = image_processor.preprocess_image(tmp_file_path)
                result = await model.analyze_image(processed_image)
                tb_analysis = tb_analyzer.analyze_for_tb(result)
                
                results.append({
                    "filename": file.filename,
                    "success": True,
                    "analysis": {
                        "raw_report": result,
                        "tb_analysis": tb_analysis,
                        "confidence": tb_analysis.get("confidence", 0.0)
                    }
                })
                
            finally:
                os.unlink(tmp_file_path)
                
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return JSONResponse({
        "success": True,
        "results": results,
        "total_processed": len(results),
        "disclaimer": "These analyses are for research purposes only and should not be used for medical diagnosis."
    })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )