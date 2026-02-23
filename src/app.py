from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI, Request

from core.config import settings
from core.logging import logger
from integrations.telegram.bot import bot, dp
from integrations.telegram.handlers.commands import command_router
from integrations.telegram.handlers.messages import messages_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Приложение запущено...")

    # При запуске приложения устанавливаем webhook телеграмм
    await bot.set_webhook(
        url=str(settings.bot_webhook_url),
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types(),
    )

    # Сохраняем бота в state приложения
    app.state.bot = bot

    yield

    logger.info("Приложение остановлено...")

    # Закрываем соединение с ботом
    # await bot.delete_webhook() # удаляем webhook по желанию
    await bot.session.close()


app = FastAPI(
    version="0.0.1",
    lifespan=lifespan,
)


dp.include_router(command_router)
dp.include_router(messages_router)


@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {
        "status": "running",
    }


@app.post(settings.tg.WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(request: Request):
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
