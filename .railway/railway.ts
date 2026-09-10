import { service } from "@railway/iac"; // Asegúrate de importar el SDK de Railway

export const apiService = service("mi-api", {
  // Configuración de construcción (Build)
  // Nota: Railpack reemplaza a Nixpacks automáticamente de forma más eficiente
  builder: "RAILPACK", 

  // Configuración de despliegue (Deploy)
  start: "uvicorn app_3:app --host 0.0.0.0 --port $PORT",
  
  replicas: 1,
  
  healthcheck: {
    path: "/health",
    timeoutSeconds: 200,
  },

  // Políticas de reinicio
  restartPolicy: {
    condition: "ON_FAILURE",
    maxRetries: 1,
  },
});