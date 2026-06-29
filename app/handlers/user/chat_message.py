import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.admin.select import get_admins
from app.database.requests.user.add import set_user
from app.database.requests.user.select import get_user
from app.database.requests.user_task.select import get_top_users

from app.filters.chat_type import ChatTypeFilter

from config import config

chat = Router()


@chat.message(Command("profile"), ChatTypeFilter(["group", "supergroup"]))
async def profile(message: Message):
    if message.chat.id != config.bot.chat_id:
        return

    tg_id = message.from_user.id
    user_info = await get_user(tg_id)

    await message.answer(
        f"<b>Профиль пользователя</b>\n\n"
        f"<b>Имя:</b> {message.from_user.full_name}\n"
        f"<b>Баланс:</b> {user_info.balance} DRPY\n"
        f"<b>Ранг:</b> {user_info.rank_name}\n\n"
        f"<b>Ты с нами с {user_info.created_at}!</b>"
    )


@chat.message(Command("top"), ChatTypeFilter(["group", "supergroup"]))
async def top(message: Message):
    if message.chat.id != config.bot.chat_id:
        return

    top_day = await get_top_users("day")
    top_week = await get_top_users("week")
    top_all = await get_top_users("all")

    def format_top(title, data):
        text = f"<b>{title}</b>\n"

        if not data:
            return text + "Нет данных\n\n"

        medals = ["🥇", "🥈", "🥉"]

        for i, (name, tg_id, points) in enumerate(data, start=1):
            medal = medals[i - 1] if i <= 3 else f"{i}."
            text += f"{medal} {name} — {points} StreetCredits\n"

        return text + "\n"

    text = (
        "🏆 <b>Рейтинг пользователей</b>\n\n"
        + format_top("📅 За сегодня", top_day)
        + format_top("📊 За неделю", top_week)
        + format_top("🔥 За всё время", top_all)
    )

    await message.answer(text)