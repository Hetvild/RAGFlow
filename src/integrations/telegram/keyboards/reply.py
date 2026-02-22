from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Основное меню бота"""
    builder = ReplyKeyboardBuilder()

    builder.button(text="👤 Профиль")
    builder.button(text="📄 Загрузить документы")
    builder.button(text="⚙️ Настройки")
    builder.button(text="📚 Справка")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
