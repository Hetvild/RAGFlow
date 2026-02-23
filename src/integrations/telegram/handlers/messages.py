from aiogram import Router, types
from aiogram.enums import ParseMode

from core.logging import logger
from services.llm_service import llm_service


messages_router = Router()


@messages_router.message()
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

    # response = await llm_service.generate_response(
    #     system_prompt="Ты полезный ассистент. Отвечай кратко.",
    #     user_message=message.text,
    #     # context="RAG (Retrieval-Augmented Generation) — это подход, который комбинирует поиск информации с генерацией текста.",
    # )

    await message.answer(
        text="Тут вернется ответ от llm", parse_mode=ParseMode.MARKDOWN
    )
