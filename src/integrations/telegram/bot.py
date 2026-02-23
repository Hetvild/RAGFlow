from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import settings


# Создаем базовый экземпляр Телеграмм бота
bot = Bot(
    token=str(settings.tg.TELEGRAM_TOKEN),
    default_properties=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
