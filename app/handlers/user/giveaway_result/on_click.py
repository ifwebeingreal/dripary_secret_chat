from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

import app.keyboards.inline as ikb
from app.database.requests.giveaway_result.select import get_giveaway_result_by_id


async def on_back(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.back()


async def on_back_menu(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager
):
    await dialog_manager.done()

    try:
        await callback.message.edit_text(
            "Поднять авторитет на блоке", reply_markup=ikb.user_panel
        )
    except Exception as e:
        print(e)

        await callback.answer()
        await callback.message.delete()

        await callback.message.answer(
            "Поднять авторитет на блоке", reply_markup=ikb.user_panel
        )


async def on_giveaway(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    giveaway_id: int,
):
    giveaway = await get_giveaway_result_by_id(int(giveaway_id))

    if not giveaway:
        await callback.answer(
            "Тут пока ничего нет, но скоро появится😉", show_alert=True
        )
        return  # 🔴 Обязательно!

    dialog_manager.dialog_data.update(giveaway_id=int(giveaway_id))

    await dialog_manager.next()
