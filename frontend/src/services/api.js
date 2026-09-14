import axios from "axios";

const api = axios.create({
  baseURL: "",
  timeout: 30000,
  headers: {"Content-Type": "application/json"}
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      const url = error.config?.url || "";
      if (!url.includes("/api/auth/login/") && !url.includes("/api/auth/register/")) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");
      }
    }
    return Promise.reject(error);
  }
);

export default api;
