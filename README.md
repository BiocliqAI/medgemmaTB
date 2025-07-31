# Chest X-ray TB Detector with MedGemma-4B

A web-based tuberculosis detection system using Google's MedGemma-4B multimodal AI model.

## ⚠️ Medical Disclaimer
**This application is for research and educational purposes only. It is NOT clinical-grade and should NOT be used for medical diagnosis. Always consult qualified healthcare professionals for medical advice.**

## Features

- Upload chest X-ray images for TB screening
- AI-powered analysis using MedGemma-4B
- Web-based interface for easy access
- Confidence scoring and validation
- Secure image handling

## Architecture

```
├── backend/          # FastAPI backend with MedGemma-4B
├── frontend/         # React web application
├── models/           # Model configurations and cache
├── docker/           # Docker deployment files
└── tests/            # Test files
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Hugging Face API Token (free)

### Setup Instructions

1. **Get Hugging Face API Token**:
   - Visit https://huggingface.co/settings/tokens
   - Create a new token with "Read" permissions
   - Accept the model license at https://huggingface.co/google/medgemma-4b-it

2. **Clone and setup**:
```bash
git clone <repository>
cd MedGemma
```

3. **Configure environment**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Hugging Face token
HUGGINGFACE_API_TOKEN=your_token_here
```

4. **Backend setup**:
```bash
cd backend
pip install -r requirements.txt
```

5. **Frontend setup**:
```bash
cd frontend
npm install
```

### Running the Application

**Option 1: Development Mode**
```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

**Option 2: Docker (Recommended)**
```bash
# Set your HF token in environment
export HUGGINGFACE_API_TOKEN=your_token_here

# Start with Docker Compose
docker-compose up -d
```

3. **Access the application** at `http://localhost:3000`

## Model Access

This project uses Google's MedGemma-4B via Hugging Face Inference API:
- **No local GPU/memory required** - runs entirely through API calls
- **Free tier available** - Hugging Face provides free inference for public models
- **Model**: `google/medgemma-4b-it`
- **Requirements**: Hugging Face account and API token

## Important Notes

- **No Local Resources**: Uses Hugging Face API - no GPU/memory requirements
- **Free to Use**: Runs on Hugging Face's free inference tier
- **TB Detection Limitation**: MedGemma-4B has known issues with TB detection accuracy
- **Privacy**: Images are sent to Hugging Face API for processing
- **Rate Limits**: Free tier has usage limits; consider Pro account for heavy usage
- **Cold Starts**: First API call may take longer as model loads on HF servers

## License

Research and educational use only. Commercial use requires appropriate medical device regulations compliance.