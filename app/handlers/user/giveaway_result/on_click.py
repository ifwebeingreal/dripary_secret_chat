from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

import app.keyboards.inline as ikb
from app.database.requests.giveaway_result.select import get_giveaway_result_by_id

from app.states import GiveawaySG


async def on_back(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.back()


async def on_back_menu(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager
):
    await dialog_manager.done()

    await callback.message.edit_text(
        "Поднять авторитет на блоке", reply_markup=ikb.user_panel
    )


async def on_giveaway(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    giveaway_id: int,
):
    giveaway = await get_giveaway_result_by_id(giveaway_id)

    if not giveaway:
        await callback.answer(
            "Тут пока ничего нет, но скоро появится😉", show_alert=True
        )
        return  # 🔴 Обязательно!

    dialog_manager.dialog_data.update(giveaway_id=giveaway_id)

    await dialog_manager.next()


async def on_figure(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, figure_id: int
):
    level_id = int(dialog_manager.dialog_data.get("skate_level_id"))
    tricks = await get_tricks_by_level_id_and_figure_id(level_id, int(figure_id))

    if not tricks:
        await callback.answer(
            "Тут пока ничего нет, но скоро появится😉", show_alert=True
        )
        return

    dialog_manager.dialog_data.update(figure_id=figure_id)
    await dialog_manager.next()


async def on_one_list(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager
):
    dialog_manager.dialog_data.update(visual=False)
    await dialog_manager.next()


async def on_nine_in_one(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager
):
    dialog_manager.dialog_data.update(visual=True)
    await dialog_manager.next()


async def on_trick(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, trick_id: int
):
    trick = await get_trick_by_id(int(trick_id))
    order = await get_order(callback.from_user.id, int(trick_id))
    subscription = await get_subscription(callback.from_user.id)

    if not trick:
        await callback.answer(
            "Тут пока ничего нет, но скоро появится😉", show_alert=True
        )
        return

    if order or subscription:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.next()
        return

    if trick.price:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.switch_to(UserSG.pay_menu)
        return

    dialog_manager.dialog_data.update(trick_id=trick_id)
    await dialog_manager.next()


async def on_trick_2(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, trick_id: int
):
    trick = await get_trick_by_id(int(trick_id))
    order = await get_order(callback.from_user.id, int(trick_id))
    subscription = await get_subscription(callback.from_user.id)

    if not trick:
        await callback.answer(
            "Тут пока ничего нет, но скоро появится😉", show_alert=True
        )
        return

    if order or subscription:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.next()
        return

    if trick.price:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.switch_to(UserSG.pay_menu)
        return

    dialog_manager.dialog_data.update(trick_id=trick_id)
    await dialog_manager.switch_to(UserSG.trick_info)


async def on_trick_info(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager
):
    await dialog_manager.next()
