import {Box} from '@material-ui/core';
import {Alert, AlertTitle} from '@mui/material';
import React from 'react';

export const UnderConstruction: React.FC<{
  title?: string;
  message?: React.ReactNode;
}> = props => {
  return (
    <Box
      sx={{
        height: '100%',
        width: '100%',
        p: 2,
      }}>
      <Alert severity="info">
        <AlertTitle>Under Construction: {props.title}</AlertTitle>
        {props.message}
      </Alert>
    </Box>
  );
};
