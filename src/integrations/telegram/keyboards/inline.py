# 1. Фабрика для передачи данных в кнопках
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallback(CallbackData, prefix="menu"):
    action: str  # Например: 'demo', 'my_bases', 'profile'
    data: str | None = None  # Дополнительные данные (например, ID базы)


# 2. Функция создания клавиатуры
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Демо базы",
                    callback_data=MenuCallback(action="demo").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📂 Мои базы",
                    callback_data=MenuCallback(action="my_bases").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📊 Лимиты", callback_data=MenuCallback(action="limits").pack()
                ),
                InlineKeyboardButton(
                    text="👤 Профиль",
                    callback_data=MenuCallback(action="profile").pack(),
                ),
            ],
        ],
        resize_keyboard=True,  # Адаптивный размер
    )
    return keyboard
