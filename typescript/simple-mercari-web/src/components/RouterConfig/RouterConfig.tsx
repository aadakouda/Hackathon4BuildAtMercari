import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Login } from "../Login";
import { SignUp } from "../SignUp";
import { Home } from "../Home";
import { Content } from "../Content";
import { ItemDetail } from "../Item";

export const RouterConfig: React.FC<{}> = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/content" element={<Content />} />
        <Route path="/content/item">
          <Route path=":id" element={<ItemDetail />} />
        </Route>
      </Routes>
    </Router>
  );
};
