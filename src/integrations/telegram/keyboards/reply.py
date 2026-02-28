from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Основное меню бота"""
    builder = ReplyKeyboardBuilder()

    builder.button(text="📚 Выбрать Демо-базу")
    builder.button(text="📂 Мои базы")
    builder.button(text="📊 Лимиты и Тариф")
    builder.button(text="⚙️ Настройки")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_stage_menu_keyboard() -> ReplyKeyboardMarkup:
    """Меню состояния диалога, активируется после выбора базы"""
    builder = ReplyKeyboardBuilder()

    builder.button(text="💬 Поле ввода")
    builder.button(text="🔄 Сменить базу")
    builder.button(text="🧹 Новый диалог")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_loadfile_menu_keyboard() -> ReplyKeyboardMarkup:
    """Меню вызывается внутри Мои базы, просит прислать файлы"""
    builder = ReplyKeyboardBuilder()

    builder.button(text="✅ Готово")
    builder.button(text="❌ Отмена")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_dialog_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="🛑 Завершить диалог")

    builder.adjust(1)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True,
        input_field_placeholder="Введите ваш вопрос...",
    )


def get_main_reply_keyboard() -> ReplyKeyboardRemove:
    """
    Удаляем клавиатуру
    :return:
    """
    return ReplyKeyboardRemove()
