from contextlib import suppress

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from integrations.telegram.keyboards.inline import (
    MenuCallback,
    get_loadfile_menu_keyboard,
    get_main_menu_keyboard,
)


bases_router = Router()


@bases_router.callback_query(MenuCallback.filter(F.action == "demo"))
async def process_demo_callback(
    callback: types.CallbackQuery, callback_data: MenuCallback
):
    await callback.answer()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text="📚 <b>Демо базы</b>\n\nВыберите базу для диалога:",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )


@bases_router.callback_query(MenuCallback.filter(F.action == "my_bases"))
async def process_my_bases_callback(
    callback: types.CallbackQuery, callback_data: MenuCallback
):
    await callback.answer()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text="📂 <b>Мои базы</b>\n\nЗдесь вы можете создать или выбрать свою базу.",
            reply_markup=get_loadfile_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
