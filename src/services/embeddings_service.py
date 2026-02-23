from typing import List

from gigachat import GigaChat
from gigachat.models import Embedding as EmbeddingsResponse
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from core.config import settings
from core.logging import logger
from utils.text_splitter import generate_chunk_id


class EmbeddingsService:
    def __init__(self):
        self.api_key = settings.GIGACHAT_API_KEY
        self.model = settings.EMBEDDINGS_MODEL
        self.collection_name = settings.QDRANT_COLLECTION_NAME

        # Инициализируем асинхронный GigaChat клиент для эмбеддингов
        self.gigachat = GigaChat(
            credentials=self.api_key, model=self.model, verify_ssl_certs=False
        )

        # Создаем клиент Qdrant
        self.client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            # api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True,
        )

    async def index_documents(self, documents: List[str]) -> int:
        """
        Генерирует эмбеддинги для списка документов и сохраняет их в Qdrant.

        Args:
            documents (List[str]): Список текстов (чанков)

        Returns:
            int: Количество добавленных точек
        """
        # Генерация эмбеддингов через GigaChat API
        response: EmbeddingsResponse = await self.gigachat.embeddings(documents)
        vectors = [item.embedding for item in response.data]

        vector_size = len(vectors[0])
        logger.info("Размер вектора: {}", vector_size)

        # Проверка и создание коллекции, если не существует
        collections = await self.client.get_collections()
        if self.collection_name not in [col.name for col in collections.collections]:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

        # Формирование точек
        points = [
            PointStruct(
                id=generate_chunk_id(document, i),
                vector=vector,
                payload={"text": document},
            )
            for i, (document, vector) in enumerate(zip(documents, vectors))
        ]

        logger.info("Точек для записи: {}", len(points))

        # Загрузка в Qdrant
        await self.client.upsert(collection_name=self.collection_name, points=points)

        return len(points)

    async def search_similar(
        self, query: str, limit: int = 3, score_threshold: float = 0.6
    ) -> List[str]:
        """
        Поиск похожих документов по запросу.

        Args:
            query (str): Текст запроса
            limit (int): Максимальное количество результатов
            score_threshold (float): Порог схожести

        Returns:
            List[str]: Список текстов из payload
        """
        # Генерация эмбеддинга для запроса
        response: EmbeddingsResponse = await self.gigachat.embeddings([query])
        query_vector = response.data[0].embedding

        # Поиск в Qdrant
        results = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
        )

        return [hit.payload["text"] for hit in results.points]
