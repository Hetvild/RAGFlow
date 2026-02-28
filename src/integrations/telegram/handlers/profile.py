from contextlib import suppress

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest  # Импортируем ошибку

from integrations.telegram.keyboards.inline import MenuCallback, get_main_menu_keyboard


profile_router = Router()


@profile_router.callback_query(MenuCallback.filter(F.action == "profile"))
async def process_profile_callback(
    callback: types.CallbackQuery, callback_data: MenuCallback
):
    await callback.answer()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=(
                f"👤 <b>Профиль</b>\n\n"
                f"ID: {callback.from_user.id}\n"
                f"Имя: {callback.from_user.username}"
            ),
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )


@profile_router.callback_query(MenuCallback.filter(F.action == "limits"))
async def process_limits_callback(
    callback: types.CallbackQuery, callback_data: MenuCallback
):
    await callback.answer()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text="📊 <b>Ваши лимиты</b>\n\nОстаток токенов: 1000",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
