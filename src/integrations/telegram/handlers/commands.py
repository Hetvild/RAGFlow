from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from core.logging import logger
from integrations.telegram.keyboards.reply import get_main_menu_keyboard
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
