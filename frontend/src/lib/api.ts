import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE ?? "/api",
  withCredentials: true,
  timeout: 15000
});

export interface HealthResponse {
  status: string;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await api.get<HealthResponse>("/health/");
  return response.data;
}

export default api;
