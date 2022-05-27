import React, { useState } from "react";
import Button from "@mui/material/Button";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { styled } from "@mui/material/styles";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

const theme = createTheme({
  palette: {
    primary: {
      main: "#eff7ff",
    },
  },
});
const Form = styled("form")(({ theme }) => ({
  display: "flex",
  gap: 5,
  marginBottom: 5,
  [theme.breakpoints.up("sm")]: {
    maxHeight: 30,
  },
  [theme.breakpoints.down("sm")]: {
    flexDirection: "column",
  },
}));

export const Listing: React.FC<{}> = () => {
  return (
    <div className="Listing">
      <Form>
        <input type="text" name="name" id="name" placeholder="name" required />
        <select
          name="category_id"
          id="category_id"
          placeholder="category_id"
          required
        >
          <option value="">--categories--</option>
          <option key={1} value={1}>
            fashion
          </option>
          <option key={2} value={2}>
            furniture
          </option>
          <option key={3} value={3}>
            kitchen
          </option>
        </select>
        <input
          type="text"
          name="price"
          id="price"
          placeholder="price"
          required
        />
        <ThemeProvider theme={theme}>
          <Button variant="contained" component="label">
            Upload File
            <input
              type="file"
              name="image"
              id="image"
              placeholder="image"
              accept="image/jpeg"
              required
              hidden
            />
          </Button>
          <FormControlLabel
            control={<Checkbox sx={{ color: "#eff7ff" }} />}
            label="private"
          />
          <FormControlLabel
            control={<Checkbox sx={{ color: "#eff7ff" }} />}
            label="barter"
          />
          <Button type="submit" variant="contained" size="small">
            List this item
          </Button>
        </ThemeProvider>
      </Form>
    </div>
  );
};
