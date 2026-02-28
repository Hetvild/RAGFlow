from contextlib import asynccontextmanager
from datetime import timedelta

from aiogram import Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI, Request

from core.config import settings
from core.logging import logger
from core.qdrant import qdrant_manager
from core.redis import redis_manager
from db.db_helper import db_helper
from integrations.telegram.bot import bot
from integrations.telegram.handlers.bases_manage import bases_router
from integrations.telegram.handlers.commands import command_router
from integrations.telegram.handlers.dialog import dialog_router
from integrations.telegram.handlers.messages import messages_router
from integrations.telegram.handlers.profile import profile_router
from integrations.telegram.middlewares.db import DatabaseMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Приложение запущено...")

    # Открываем подключение к Redis
    await redis_manager.connect()

    # Открываем подключение к Qdrant
    await qdrant_manager.connect()

    storage = RedisStorage(
        redis=redis_manager.get_client(),
        state_ttl=timedelta(minutes=30),  # Настоящее время жизни состояний
        data_ttl=timedelta(minutes=30),  # Настоящее время жизни данных
        # ⬇ Префиксы задаются отдельно, если нужно (опционально)
        key_builder=None,  # Можно использовать DefaultKeyBuilder для кастомных префиксов
    )
    # Создаем новый диспетчер с RedisStorage
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DatabaseMiddleware())

    # Подключаем роутеры Aiogram
    dp.include_router(dialog_router)
    dp.include_router(bases_router)
    dp.include_router(profile_router)
    dp.include_router(command_router)
    dp.include_router(messages_router)

    # При запуске приложения устанавливаем webhook телеграмм
    await bot.set_webhook(
        url=str(settings.bot_webhook_url),
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types(),
    )

    # Сохраняем бота и диспетчер в state приложения
    app.state.bot = bot
    app.state.dp = dp

    yield

    logger.info("Приложение остановлено...")

    # Закрываем соединение с ботом
    await bot.session.close()

    # Закрываем подключение к Redis
    await redis_manager.disconnect()

    # Закрываем подключение к Qdrant
    await qdrant_manager.disconnect()

    await db_helper.dispose()  # <--- Добавляем закрытие пула Postgres


app = FastAPI(
    version="0.0.1",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {
        "status": "running",
    }


@app.post(settings.tg.WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(request: Request):
    # Получаем бота и диспетчер из state приложения
    bot = app.state.bot
    dp = app.state.dp

    # Получаем JSON от Телеграмм
    update_data = await request.json()

    # Преобразуем JSON в объект Update aiogram
    update = types.Update.model_validate(update_data, context={"bot": bot})

    # Пробрасываем обновление в диспетчер
    await dp.feed_update(
        bot,
        update,
    )
    return {"ok": True}
