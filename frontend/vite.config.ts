import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  const backendHost = env.BACKEND_HOST || "127.0.0.1";
  const backendPort = env.BACKEND_PORT || "8000";
  const backendOrigin = env.BACKEND_ORIGIN || `http://${backendHost}:${backendPort}`;
  const frontendHost = env.FRONTEND_HOST || "127.0.0.1";
  const frontendPort = Number(env.FRONTEND_PORT || env.PORT || "5173");

  return {
    esbuild: {
      jsx: "automatic",
      jsxImportSource: "react"
    },
    optimizeDeps: {
      include: ["react", "react-dom"]
    },
    server: {
      host: frontendHost,
      port: frontendPort,
      strictPort: true,
      proxy: {
        "/api": {
          target: backendOrigin,
          changeOrigin: true
        }
      }
    }
  };
});
