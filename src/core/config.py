# Создаем базовую конфигурацию через pydantic-settings
from pathlib import Path
from urllib.parse import urljoin

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Определяем путь к корню проекта (на 2 уровня выше, чем этот файл)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class TelegramConfig(BaseModel):
    TELEGRAM_TOKEN: str
    WEBHOOK_PATH: str


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

    LLM_API_KEY: str
    LLM_BASE_URL: str
    LLM_MODEL_NAME: str
    LLM_TEMPERATURE: float = 0.7

    GIGACHAT_API_KEY: str | None = None
    EMBEDDINGS_MODEL: str = "EmbeddingsGigaR"

    QDRANT_COLLECTION_NAME: str = "Rag"
    QDRANT_URL: str = "http://localhost:6333"

    tg: TelegramConfig = None

    @computed_field
    def bot_webhook_url(self) -> str:
        return urljoin(str(self.BASE_URL), str(self.tg.WEBHOOK_PATH))


settings = Settings()
