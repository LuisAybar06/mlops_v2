import { defineRailway, project, service } from "railway/iac";

export default defineRailway(() => {
  const api = service("mi-api", {
    start: "uvicorn app_3:app --host 0.0.0.0 --port $PORT",
    replicas: 1,
    healthcheck: "/health",
  });

  return project("sesion-3-v2", {
    resources: [api],
  });
});