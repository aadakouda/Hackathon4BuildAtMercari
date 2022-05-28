import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import AccountCircle from "@mui/icons-material/AccountCircle";
import Avatar from "@mui/material/Avatar";
import MenuItem from "@mui/material/MenuItem";
import Logout from "@mui/icons-material/Logout";
import Divider from "@mui/material/Divider";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Menu from "@mui/material/Menu";
const theme = createTheme({
  palette: {
    primary: {
      main: "#222427",
    },
  },
});

export const MenuAppBar: React.FC<{}> = () => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
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
            <div>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle fontSize="inherit" />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem sx={{ width: 160,gap:1}} onClick={handleClose}>
                  <Avatar sx={{ width: 24, height: 24 }} />
                  Profile
                </MenuItem>
                <MenuItem sx={{ gap: 1 }} onClick={handleClose}>
                  <Avatar sx={{ width: 24, height: 24 }}/>
                  My account
                </MenuItem>
                <Divider />
                <MenuItem sx={{ gap: 1 }} onClick={handleClose}>
                  <Logout sx={{ ml: 0.5 }}fontSize="small" />
                  Logout
                </MenuItem>
              </Menu>
            </div>
          </Toolbar>
        </AppBar>
      </ThemeProvider>
    </Box>
  );
};
