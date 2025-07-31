import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Paper,
  Typography,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import { CloudUpload, Image as ImageIcon } from '@mui/icons-material';

const ImageUploader = ({ onImageUpload, loading }) => {
  const [preview, setPreview] = useState(null);
  const [file, setFile] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      alert('Please upload a valid image file (JPG, PNG, BMP, TIFF)');
      return;
    }

    const uploadedFile = acceptedFiles[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(uploadedFile);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.tiff']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleAnalyze = () => {
    if (file && onImageUpload) {
      onImageUpload(file);
    }
  };

  const handleReset = () => {
    setPreview(null);
    setFile(null);
  };

  return (
    <Box sx={{ textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom color="primary">
        Chest X-ray TB Detection
      </Typography>
      <Typography variant="body1" gutterBottom color="textSecondary" sx={{ mb: 3 }}>
        Upload a chest X-ray image for tuberculosis screening analysis
      </Typography>

      {!preview ? (
        <Paper
          {...getRootProps()}
          sx={{
            p: 4,
            border: '2px dashed',
            borderColor: isDragActive ? 'primary.main' : 'grey.400',
            backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            '&:hover': {
              borderColor: 'primary.main',
              backgroundColor: 'action.hover',
            },
          }}
        >
          <input {...getInputProps()} />
          <CloudUpload sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            {isDragActive
              ? 'Drop the image here...'
              : 'Drag & drop a chest X-ray image here'}
          </Typography>
          <Typography variant="body2" color="textSecondary" gutterBottom>
            or click to select a file
          </Typography>
          <Typography variant="caption" color="textSecondary">
            Supported formats: JPG, PNG, BMP, TIFF (max 10MB)
          </Typography>
        </Paper>
      ) : (
        <Box>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <ImageIcon sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6">
                Preview: {file?.name}
              </Typography>
            </Box>
            <Box
              component="img"
              src={preview}
              alt="Chest X-ray preview"
              sx={{
                maxWidth: '100%',
                maxHeight: 400,
                objectFit: 'contain',
                border: '1px solid',
                borderColor: 'grey.300',
                borderRadius: 1,
              }}
            />
          </Paper>

          <Alert severity="info" sx={{ mb: 3 }}>
            <Typography variant="body2">
              The image will be analyzed using MedGemma-4B for potential tuberculosis indicators. 
              This process may take 30-60 seconds depending on your system capabilities.
            </Typography>
          </Alert>

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="contained"
              size="large"
              onClick={handleAnalyze}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <CloudUpload />}
            >
              {loading ? 'Analyzing...' : 'Analyze for TB'}
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={handleReset}
              disabled={loading}
            >
              Choose Different Image
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default ImageUploader;