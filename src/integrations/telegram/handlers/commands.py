from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from core.logging import logger
from integrations.telegram.keyboards.inline import MenuCallback, get_main_menu_keyboard
from integrations.telegram.messages.text import START_MESSAGE


command_router = Router()


@command_router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    full_name = message.from_user.full_name
    message_text = message.text
    logger.debug(
        "User_id: {}, Username: {}, Firstname: {}, Lastname: {}, Fullname: {}, Textmessage: {}",
        user_id,
        user_name,
        first_name,
        last_name,
        full_name,
        message_text,
    )

    await message.answer(
        text=START_MESSAGE,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard(),
    )


# 2. Обработчик нажатий на кнопки меню
@command_router.callback_query(MenuCallback.filter())
async def process_menu_callback(
    callback: types.CallbackQuery, callback_data: MenuCallback
):

    # Отвечаем на callback (обязательно, чтобы убрать часы загрузки у пользователя)
    await callback.answer()
    action = callback_data.action

    if action == "demo":
        await callback.message.edit_text(
            text="📚 <b>Демо базы</b>\n\nВыберите базу для диалога:",
            reply_markup=get_main_menu_keyboard(),  # Здесь можно подключить другую клавиатуру со списком баз
            parse_mode=ParseMode.HTML,
        )
    elif action == "my_bases":
        await callback.message.edit_text(
            text="📂 <b>Мои базы</b>\n\nЗдесь вы можете создать или выбрать свою базу.",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
    elif action == "limits":
        await callback.message.edit_text(
            text="📊 <b>Ваши лимиты</b>\n\nОстаток токенов: 1000",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
    elif action == "profile":
        await callback.message.edit_text(
            text="👤 <b>Профиль</b>\n\nID: " + str(callback.from_user.id),
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
