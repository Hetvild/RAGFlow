from aiogram import F, Router, types
from aiogram.enums import ParseMode

from core.logging import logger
from integrations.telegram.keyboards.inline import get_main_menu_keyboard


messages_router = Router()


@messages_router.message(F.text)
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
        text="Выберете из меню что вы хотите сделать",
        reply_markup=get_main_menu_keyboard(),
        parse_mode=ParseMode.MARKDOWN,
    )
