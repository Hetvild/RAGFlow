from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

from core.config import settings
from core.logging import logger


class QdrantManager:
    def __init__(self):
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._client: AsyncQdrantClient | None = None

    async def connect(self):
        """Инициализация подключения к Qdrant"""
        if self._client is None:
            self._client = AsyncQdrantClient(
                url=settings.QDRANT_URL,
                prefer_grpc=True,
                timeout=settings.QDRANT_TIMEOUT,
            )

        # Проверяем соединение
        try:
            await self._client.get_collections()
            logger.debug("Qdrant connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise

        # Создаем коллекцию, если не существует
        await self._create_collection_if_not_exists()

    async def disconnect(self):
        """Закрытие подключения к Qdrant"""
        if self._client is not None:
            await self._client.close()
            logger.debug("Qdrant disconnected")

    async def _create_collection_if_not_exists(self):
        """Создает коллекцию, если она ещё не существует"""
        collections = await self._client.get_collections()
        collection_names = [c.name for c in collections.collections]

        if self.collection_name not in collection_names:
            await self._client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.QDRANT_VECTOR_SIZE,  # должно быть в settings
                    distance=Distance.COSINE,  # или настраиваемо
                ),
            )
            logger.info(f"Qdrant collection '{self.collection_name}' created")
        else:
            logger.debug(f"Qdrant collection '{self.collection_name}' already exists")

    def get_client(self) -> AsyncQdrantClient:
        """
        Возвращает клиент для прямого использования (в репозиториях и т.п.)
        """
        if self._client is None:
            raise RuntimeError("Qdrant not connected")
        return self._client


qdrant_manager = QdrantManager()
