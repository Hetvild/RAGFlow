from typing import List

from gigachat import GigaChat
from gigachat.models import Embedding as EmbeddingsResponse
from qdrant_client.models import PointStruct

from core.config import settings
from core.logging import logger
from db.repositories.vector_repo import VectorRepository
from utils.text_splitter import generate_chunk_id


class EmbeddingsService:
    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo  # <--- Теперь мы принимаем репозиторий извне
        self.api_key = settings.GIGACHAT_API_KEY
        self.model = settings.EMBEDDINGS_MODEL

        # Инициализируем GigaChat клиент (его можно оставить здесь, так как он специфичен для этого сервиса)
        self.gigachat = GigaChat(
            credentials=self.api_key, model=self.model, verify_ssl_certs=False
        )

    async def index_documents(self, documents: List[str]) -> int:
        """
        Генерирует эмбеддинги для списка документов и сохраняет их в Qdrant.
        """
        # 1. Генерация эмбеддингов через GigaChat API
        response: EmbeddingsResponse = await self.gigachat.embeddings(documents)
        vectors = [item.embedding for item in response.data]

        logger.info("Размер вектора: {}", len(vectors[0]))

        # 2. Формирование точек для Qdrant
        points = [
            PointStruct(
                id=generate_chunk_id(document, i),
                vector=vector,
                payload={"text": document},
            )
            for i, (document, vector) in enumerate(zip(documents, vectors))
        ]

        logger.info("Точек для записи: {}", len(points))

        # 3. Сохранение через репозиторий
        return await self.vector_repo.upsert_points(points)

    async def search_similar(
        self, query: str, limit: int = 3, score_threshold: float = 0.6
    ) -> List[str]:
        """
        Поиск похожих документов по запросу.
        """
        # 1. Генерация эмбеддинга для текстового запроса
        response: EmbeddingsResponse = await self.gigachat.embeddings([query])
        query_vector = response.data[0].embedding

        # 2. Поиск через репозиторий
        return await self.vector_repo.search_similar(
            query_vector=query_vector, limit=limit, score_threshold=score_threshold
        )
