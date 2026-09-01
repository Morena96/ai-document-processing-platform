from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Document Processing Platform"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/documents"
    redis_url: str = "redis://localhost:6379/0"
    storage_path: str = "/tmp/document-platform"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
