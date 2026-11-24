from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/task_manager"
    secret_key: str = "change-this-secret-key-before-deploying"
    access_token_expire_minutes: int = 60
    redis_url: str = "redis://redis:6379/0"
    cors_origins_raw: str = "http://localhost:8000"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
