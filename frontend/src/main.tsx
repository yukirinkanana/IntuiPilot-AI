import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

const container = document.getElementById("root");

if (!container) {
  throw new Error("未找到 root 容器");
}

createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>
);
