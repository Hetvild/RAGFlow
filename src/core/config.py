# Создаем базовую конфигурацию через pydantic-settings
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Определяем путь к корню проекта (на 2 уровня выше, чем этот файл)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.dev",
            BASE_DIR / ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    # Подключаем базовую конфигурацию
    LOG_LEVEL: str = "INFO"

    GIGACHAT_API_KEY: str | None = None
    EMBEDDINGS_MODEL: str = "EmbeddingsGigaR"
    QDRANT_COLLECTION_NAME: str = "Rag"
    QDRANT_URL: str = "http://localhost:6333"


settings = Settings()
