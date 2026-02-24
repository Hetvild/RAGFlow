from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.qdrant import qdrant_manager
from db.db_helper import db_helper
from db.repositories.user_repo import UserRepository
from db.repositories.vector_repo import VectorRepository
from services.embeddings_service import EmbeddingsService


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        # Получаем клиента Qdrant
        qdrant_client = qdrant_manager.get_client()

        # Инициализируем репозиторий Qdrant и Сервис
        vector_repo = VectorRepository(qdrant_client)
        embeddings_service = EmbeddingsService(vector_repo)

        # Открываем сессию Postgres для этого конкретного апдейта
        async for session in db_helper.get_session():
            # Инициализируем репозиторий юзеров
            user_repo = UserRepository(session)

            # Прокидываем в словарь data, который будет доступен в хэндлерах
            data["user_repo"] = user_repo
            data["embeddings_service"] = embeddings_service

            # Передаем управление хэндлеру
            return await handler(event, data)
