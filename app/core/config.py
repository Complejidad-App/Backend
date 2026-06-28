from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "Complejidad App API"
    API_V1_PREFIX: str = "/api/v1"

    # Ruta al dataset de edgelist usado por el analisis de grafo de seguidores.
    FOLLOWERS_DATASET_PATH: str = "data/tiktok_combined.txt"

    # Origenes permitidos para CORS, separados por coma en la variable de entorno.
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
