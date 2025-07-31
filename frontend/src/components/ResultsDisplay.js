import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
  Chip,
  Divider,
  Card,
  CardContent,
  LinearProgress,
  Grid
} from '@mui/material';
import {
  Refresh,
  Warning,
  CheckCircle,
  Error,
  Info
} from '@mui/icons-material';

const ResultsDisplay = ({ result, onReset }) => {
  if (!result || !result.analysis) {
    return null;
  }

  const { analysis } = result;
  const { tb_analysis } = analysis;

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel) {
      case 'high':
        return <Error color="error" />;
      case 'medium':
        return <Warning color="warning" />;
      case 'low':
        return <Info color="info" />;
      default:
        return <CheckCircle color="success" />;
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'success';
    }
  };

  const formatConfidence = (confidence) => {
    return Math.round(confidence * 100);
  };

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" color="primary">
            Analysis Results
          </Typography>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={onReset}
          >
            Analyze New Image
          </Button>
        </Box>

        <Grid container spacing={3}>
          {/* TB Risk Assessment */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {getRiskIcon(tb_analysis.tb_risk_level)}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    TB Risk Assessment
                  </Typography>
                </Box>
                
                <Chip
                  label={`${tb_analysis.tb_risk_level.toUpperCase()} RISK`}
                  color={getRiskColor(tb_analysis.tb_risk_level)}
                  variant="filled"
                  sx={{ mb: 2, fontWeight: 'bold' }}
                />

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Risk Score: {Math.round(tb_analysis.tb_risk_score * 100)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={tb_analysis.tb_risk_score * 100}
                    color={getRiskColor(tb_analysis.tb_risk_level)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>

                <Box>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Confidence: {formatConfidence(tb_analysis.confidence)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={tb_analysis.confidence * 100}
                    color="primary"
                    sx={{ height: 6, borderRadius: 3 }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Recommendation */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recommendation
                </Typography>
                <Alert
                  severity={getRiskColor(tb_analysis.tb_risk_level)}
                  sx={{ '& .MuiAlert-message': { whiteSpace: 'pre-line' } }}
                >
                  {tb_analysis.recommendation}
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Findings */}
        {tb_analysis.findings && tb_analysis.findings.length > 0 && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Key Findings
            </Typography>
            <Grid container spacing={2}>
              {tb_analysis.findings.map((finding, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card variant="outlined">
                    <CardContent sx={{ p: 2 }}>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        {finding.finding}
                      </Typography>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Location: {finding.location}
                      </Typography>
                      <Typography variant="body2" gutterBottom>
                        {finding.description}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        <Chip
                          label={`${formatConfidence(finding.confidence)}% confidence`}
                          size="small"
                          color={finding.confidence > 0.7 ? 'error' : finding.confidence > 0.5 ? 'warning' : 'default'}
                        />
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* Keywords Found */}
        {tb_analysis.keywords_found && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Analysis Keywords
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {tb_analysis.keywords_found.high_risk?.map((keyword, index) => (
                <Chip key={index} label={keyword} color="error" size="small" />
              ))}
              {tb_analysis.keywords_found.medium_risk?.map((keyword, index) => (
                <Chip key={index} label={keyword} color="warning" size="small" />
              ))}
              {tb_analysis.keywords_found.low_risk?.map((keyword, index) => (
                <Chip key={index} label={keyword} color="info" size="small" />
              ))}
            </Box>
          </Box>
        )}

        <Divider sx={{ my: 3 }} />

        {/* Full Report */}
        <Box>
          <Typography variant="h6" gutterBottom>
            Full AI Report
          </Typography>
          <Paper variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
            <Typography
              variant="body2"
              sx={{ whiteSpace: 'pre-line', fontFamily: 'monospace' }}
            >
              {analysis.raw_report}
            </Typography>
          </Paper>
        </Box>

        {/* Disclaimer */}
        <Alert severity="warning" sx={{ mt: 3 }}>
          <Typography variant="body2">
            {result.disclaimer}
          </Typography>
        </Alert>
      </Paper>
    </Box>
  );
};

export default ResultsDisplay;