from operator import itemgetter

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Column,
    Button,
    ScrollingGroup,
    Select,
    Url,
    Row,
    PrevPage,
    NextPage,
    Group,
    CurrentPage,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from app.handlers.user.giveaway_result.getters import (
    giveaways_getter,
    giveaway_info_getter,
)
from app.handlers.user.giveaway_result.on_click import (
    on_back_menu,
    on_giveaway,
    on_back,
)
from app.states import GiveawaySG

giveaway = Router()


giveaway_dialog = Dialog(
    Window(
        Const(text="Архив с розыгрышами за всю историю <b>секретной банды:</b>"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="giveaways",
                item_id_getter=itemgetter(1),
                on_click=on_giveaway,
            ),
            width=1,
            height=5,
            id="giveaways_scroll",
            hide_pager=True,
        ),
        Row(
            PrevPage(scroll="giveaways_scroll", text=Const("⬅️")),
            CurrentPage(
                scroll="giveaways_scroll",
                text=Format("{current_page + 1} / {pages}"),
            ),
            NextPage(scroll="giveaways_scroll", text=Const("➡️")),
        ),
        Column(
            Button(Const("🔙 Назад"), id="back_menu", on_click=on_back_menu),
        ),
        getter=giveaways_getter,
        state=GiveawaySG.all_giveaways,
    ),
    Window(
        DynamicMedia("file_id", when="file_id"),
        Format("<b>{title}</b>\n"),
        Format("{winners_text}\n"),
        Format("<i>Дата проведения: {created_at}</i>\n"),
        Column(
            Button(Const("🔙 Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu", on_click=on_back_menu),
        ),
        state=GiveawaySG.giveaway_info,
        getter=giveaway_info_getter,
    ),
)


@giveaway.callback_query(F.data == "all_giveaways")
async def all_giveaways_callback(
    callback: CallbackQuery, dialog_manager: DialogManager
):
    await dialog_manager.start(GiveawaySG.all_giveaways, mode=StartMode.RESET_STACK)
