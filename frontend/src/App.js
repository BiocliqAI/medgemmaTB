import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Container, Typography, Box, Alert } from '@mui/material';
import ImageUploader from './components/ImageUploader';
import ResultsDisplay from './components/ResultsDisplay';
import Header from './components/Header';
import ApiService from './services/ApiService';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = async (file) => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await ApiService.analyzeImage(file);
      setAnalysisResult(result);
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Header />
        
        <Box sx={{ mt: 4, mb: 4 }}>
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Typography variant="body2">
              <strong>Medical Disclaimer:</strong> This application is for research and educational purposes only. 
              It is NOT clinical-grade and should NOT be used for medical diagnosis. Always consult qualified 
              healthcare professionals for medical advice.
            </Typography>
          </Alert>

          {!analysisResult && (
            <ImageUploader 
              onImageUpload={handleImageUpload}
              loading={loading}
            />
          )}

          {error && (
            <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
              {error}
            </Alert>
          )}

          {analysisResult && (
            <ResultsDisplay 
              result={analysisResult}
              onReset={handleReset}
            />
          )}

          {loading && (
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Typography variant="h6" color="primary">
                Analyzing chest X-ray with MedGemma-4B...
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                This may take a few moments
              </Typography>
            </Box>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;