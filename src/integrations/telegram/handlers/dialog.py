import asyncio

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from core.config import settings
from core.logging import logger
from core.qdrant import qdrant_manager
from db.repositories.vector_repo import VectorRepository
from integrations.telegram.fsm_states import DialogStates
from integrations.telegram.keyboards.inline import MenuCallback
from integrations.telegram.keyboards.reply import (
    get_dialog_keyboard,
    get_main_reply_keyboard,
)
from services.embeddings_service import EmbeddingsService
from services.llm_service import llm_service


dialog_router = Router()


@dialog_router.callback_query(MenuCallback.filter(F.action == "start_dialog"))
async def start_dialog(
    callback: types.CallbackQuery,
    callback_data: MenuCallback,
    state: FSMContext,
):

    await callback.answer()

    # Сохраняем время старта и выбранную базу
    await state.set_state(DialogStates.active)
    await state.update_data(started_at=asyncio.get_event_loop().time())

    await callback.message.answer(
        text="💬 <b>Диалог начат.</b>\nЗадайте ваш вопрос.\n\nНажмите кнопку ниже, чтобы завершить сессию.",
        reply_markup=get_dialog_keyboard(),
        parse_mode=ParseMode.HTML,
    )


@dialog_router.message(
    DialogStates.active,
    F.text,
    ~F.text.in_({"🛑 Завершить диалог"}),
)
async def process_dialog(message: types.Message, state: FSMContext):

    # Проверяем таймауты бездействия (например 30 минут)
    data = await state.get_data()
    last_msg_time = data.get("last_msg_time", data.get("started_at", 0))
    now = asyncio.get_event_loop().time()

    if now - last_msg_time > 1800:
        await state.clear()
        await message.answer(
            "⏱ Сессия завершена по таймауту. Начните новый диалог из меню.",
            reply_markup=get_main_reply_keyboard(),
        )
        return

    await state.update_data(last_msg_time=now)

    try:
        # Получаем клиенты и сервисы
        client = qdrant_manager.get_client()
        vector_repo = VectorRepository(client=client)
        service = EmbeddingsService(vector_repo=vector_repo)

        # Поиск похожих документов
        search_results = await service.search_similar(message.text)
        logger.debug("Результат обращения к embedding: {}", search_results)

        if search_results:
            # Формируем контекст из результатов поиска
            context = "\n".join(search_results) if search_results else None

            # Отправляем вопрос из диалога в LLM с контекстом
            response = await llm_service.generate_response(
                system_prompt=settings.SYSTEM_PROMPT,
                user_message=message.text,
                context=context,
            )

            await message.answer(response, reply_markup=get_dialog_keyboard())
        else:
            await message.answer(
                "Данные в базе не найдены", reply_markup=get_dialog_keyboard()
            )

    except Exception as e:
        logger.error("Ошибка при обработке диалога: {}", e)
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Попробуйте позже.",
            reply_markup=get_dialog_keyboard(),
        )


@dialog_router.message(DialogStates.active, F.text == "🛑 Завершить диалог")
async def stop_dialog(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "✅ Диалог завершён. Возвращаемся в главное меню.",
        reply_markup=get_main_reply_keyboard(),
    )
