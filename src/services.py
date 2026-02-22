from langchain_gigachat import GigaChatEmbeddings
from qdrant_client import AsyncQdrantClient as QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from core.config import settings
from core.logging import logger
from utils.text_splitter import generate_chunk_id


class EmbeddingsService:
    def __init__(self):

        self.api_key = settings.GIGACHAT_API_KEY
        self.embeddings_model = settings.EMBEDDINGS_MODEL

        self.collection_name = settings.QDRANT_COLLECTION_NAME

        self.embeddings = GigaChatEmbeddings(
            credentials=self.api_key,
            model=self.embeddings_model,
            verify_ssl_certs=False,
        )

        # Создаем клиент Qdrant
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            # api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True,
        )

    async def index_documents(self, documents: list[str]) -> int:
        """
        Принимает список чанков и возвращает список векторов
        Использует пакетную обработку

        Args:
            documents (list[str]): Список текстов(чанков)

        Returns:
            list[list[float]]: Список векторов
        """

        # Создаем векторы для всех текстов сразу
        vectors = await self.embeddings.aembed_documents(documents)

        # Определяем размерность вектора
        vector_size = len(vectors[0])
        logger.info("Размер вектора {}", vector_size)

        # Создаем коллекцию в Qdrant если ее нет
        collections = await self.client.get_collections()
        if self.collection_name not in [col.name for col in collections.collections]:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

        # Формируем точки для записи
        points = [
            PointStruct(
                id=generate_chunk_id(document, i),
                vector=vector,
                payload={"text": document},
            )
            for i, (document, vector) in enumerate(zip(documents, vectors))
        ]

        logger.info("Точек для записи {}", len(points))

        # Записываем точки в коллекцию
        await self.client.upsert(collection_name=self.collection_name, points=points)

        return len(points)

    async def search_similar(
        self, query: str, limit: int = 3, score_threshold: float = 0.6
    ):
        """
        Принимает вопрос пользователя, находит похожие документы.
        Использует одиночную обработку запроса.
        """
        # 1. Создаем вектор для вопроса
        query_vector = await self.embeddings.aembed_query(query)

        # 2. Ищем похожие векторы в базе
        results = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,  # Фильтруем похожие документы
        )

        # 3. Возвращаем только тексты (payload)
        return [hit.payload["text"] for hit in results.points]
