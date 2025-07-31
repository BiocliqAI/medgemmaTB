import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 120000, // 2 minutes timeout for AI processing
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        
        if (error.response) {
          // Server responded with error status
          const message = error.response.data?.detail || 
                         error.response.data?.message || 
                         `Server error: ${error.response.status}`;
          throw new Error(message);
        } else if (error.request) {
          // Request made but no response received
          throw new Error('Cannot connect to the server. Please check if the backend is running.');
        } else {
          // Something else happened
          throw new Error('An unexpected error occurred');
        }
      }
    );
  }

  async checkHealth() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Health check failed: ' + error.message);
    }
  }

  async analyzeImage(file) {
    try {
      // Validate file
      if (!file) {
        throw new Error('No file provided');
      }

      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'];
      if (!allowedTypes.includes(file.type)) {
        throw new Error('Unsupported file type. Please upload a JPG, PNG, BMP, or TIFF image.');
      }

      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        throw new Error('File too large. Please upload an image smaller than 10MB.');
      }

      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      // Make API call
      const response = await this.client.post('/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload progress: ${progress}%`);
        },
      });

      return response.data;
    } catch (error) {
      console.error('Image analysis failed:', error);
      throw error;
    }
  }

  async batchAnalyze(files) {
    try {
      if (!files || files.length === 0) {
        throw new Error('No files provided');
      }

      if (files.length > 10) {
        throw new Error('Maximum 10 files allowed for batch processing');
      }

      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      const response = await this.client.post('/batch-analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minutes for batch processing
      });

      return response.data;
    } catch (error) {
      console.error('Batch analysis failed:', error);
      throw error;
    }
  }

  // Utility method to check if backend is available
  async isBackendAvailable() {
    try {
      const health = await this.checkHealth();
      return health.status === 'healthy' && health.model_status === 'loaded';
    } catch (error) {
      return false;
    }
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;