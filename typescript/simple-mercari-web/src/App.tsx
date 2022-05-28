import "./App.css";
import { RouterConfig } from "./components/RouterConfig";
import { Providers } from "./components/Providers";
function App() {
  return (
    <Providers>
      <RouterConfig />
    </Providers>
  );
}

export default App;
