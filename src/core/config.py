# Создаем базовую конфигурацию через pydantic-settings
from pathlib import Path
from urllib.parse import urljoin

from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Определяем путь к корню проекта (на 2 уровня выше, чем этот файл)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class TelegramConfig(BaseModel):
    TELEGRAM_TOKEN: str
    WEBHOOK_PATH: str


class DbConfig(BaseModel):
    DATABASE_URL: PostgresDsn


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
    BASE_URL: str = "https://api.telegram.org/bot"

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_PREFIX: str = "my_saas_project"
    REDIS_MAX_CONNECTIONS: int = 50
    REDIS_SOCKET_TIMEOUT: float = 5.0
    REDIS_SOCKET_CONNECT_TIMEOUT: float = 5.0

    LLM_API_KEY: str
    LLM_BASE_URL: str
    LLM_MODEL_NAME: str
    LLM_TEMPERATURE: float = 0.7

    GIGACHAT_API_KEY: str | None = None
    EMBEDDINGS_MODEL: str = "EmbeddingsGigaR"

    QDRANT_COLLECTION_NAME: str = "Rag"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_TIMEOUT: float = 5.0

    db: DbConfig
    tg: TelegramConfig = None

    @computed_field
    def bot_webhook_url(self) -> str:
        return urljoin(str(self.BASE_URL), str(self.tg.WEBHOOK_PATH))


settings = Settings()
