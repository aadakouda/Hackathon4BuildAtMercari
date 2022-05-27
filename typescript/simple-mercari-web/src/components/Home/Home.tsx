import React, { useState, useEffect } from "react";
import { Login } from "../Login";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
const theme = createTheme({
  palette: {
    primary: {
      main: "#222427",
    },
  },
});
export const Home: React.FC<{}> = () => {
  return (
    <div>
      <Box sx={{ flexGrow: 1 }}>
        <ThemeProvider theme={theme}>
          <AppBar position="static">
            <Toolbar>
              <Typography
                variant="h6"
                align="center"
                component="div"
                sx={{ flexGrow: 1 }}
              >
                Simple Mercari
              </Typography>
            </Toolbar>
          </AppBar>
        </ThemeProvider>
      </Box>
      <div>
        <Login />
      </div>
    </div>
  );
};
