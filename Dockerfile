# Railway Dockerfile for full-stack deployment
FROM python:3.10-slim

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend files and build
COPY frontend/ frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Copy backend code
WORKDIR /app
COPY backend/ backend/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Copy startup script
COPY start.py .
RUN chmod +x start.py

# Start the application
CMD ["python", "/app/start.py"]