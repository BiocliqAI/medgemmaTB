import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Chip 
} from '@mui/material';
import { LocalHospital } from '@mui/icons-material';

const Header = () => {
  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <LocalHospital sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          TB Detector - Chest X-ray Analysis
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip 
            label="MedGemma-4B" 
            color="secondary" 
            variant="outlined" 
            size="small"
          />
          <Chip 
            label="Research Only" 
            color="warning" 
            variant="outlined" 
            size="small"
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;