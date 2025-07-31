# Railway Dockerfile for full-stack deployment
FROM python:3.10-slim

# Install Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and build frontend
COPY frontend/package*.json frontend/
WORKDIR /app/frontend
RUN npm install

COPY frontend/ .
RUN npm run build

# Copy backend code
WORKDIR /app
COPY backend/ backend/

# Expose port (Railway will override this)
EXPOSE 8000

# Start the application
CMD ["python", "backend/main.py"]