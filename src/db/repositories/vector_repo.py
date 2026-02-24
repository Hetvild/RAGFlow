from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct

from core.config import settings


class VectorRepository:
    def __init__(self, client: AsyncQdrantClient):
        self.client = client
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    async def upsert_points(self, points: list[PointStruct]) -> int:
        """
        Сохраняет готовые точки (id, vector, payload) в Qdrant.
        Возвращает количество сохраненных точек.
        """
        await self.client.upsert(collection_name=self.collection_name, points=points)

        return len(points)

    async def search_similar(
        self, query_vector: list[float], limit: int = 3, score_threshold: float = 0.6
    ) -> list[str]:
        """
        Ищет похожие вектора и возвращает список текстов из payload.
        """
        results = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
        )

        return [hit.payload["text"] for hit in results.points]
