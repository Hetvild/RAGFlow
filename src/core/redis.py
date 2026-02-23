import redis.asyncio as redis

from core.config import settings
from core.logging import logger


class RedisManager:
    def __init__(self):
        self._client: redis.Redis | None = None
        self._pool: redis.ConnectionPool | None = None

    async def connect(self):
        """Инициализация подключения"""
        if self._pool is None:
            self._pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
                socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
                retry_on_timeout=True,
            )

        if self._client is None:
            self._client = redis.Redis(connection_pool=self._pool)

        # Проверяем соединение
        await self._client.ping()
        logger.debug("Redis connected")

    async def disconnect(self):
        if self._client:
            await self._client.close()
            await self._pool.disconnect()
            logger.debug("Redis disconnected")

    def get_pool(self) -> redis.ConnectionPool:
        """
        Возвращает пул для Aiogram Storage, он сам управляет жизненным циклом
        Нужен только пул
        """

        if self._pool is None:
            raise RuntimeError("Redis not connected")
        return self._pool

    def get_client(self) -> redis.Redis:
        """
        Создает клиент для прямого использования (Кеш, брокер)
        """
        if self._client is None:
            raise RuntimeError("Redis not connected")
        return self._client


redis_manager = RedisManager()
