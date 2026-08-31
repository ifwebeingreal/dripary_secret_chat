from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest

from app.database.models import async_session, User, Admin
from app.database.models import Giveaway
from sqlalchemy import select, func

from config import config


async def get_giveaway(id: int):
    async with async_session() as session:
        giveaway = await session.scalar(
            select(Giveaway)
            .where(Giveaway.id == id)
        )
        return giveaway


async def get_giveaway_winners(
    bot: Bot,
    giveaway_id: int,
) -> list[User]:
    async with async_session() as session:
        giveaway = await session.get(Giveaway, giveaway_id)

        if giveaway is None:
            return []

        admin_ids = select(Admin.tg_id)

        stmt = (
            select(User)
            .where(User.tg_id.not_in(admin_ids))
            .order_by(func.random())
        )

        result = await session.execute(stmt)
        users = result.scalars().all()

    winners: list[User] = []

    for user in users:
        try:
            member = await bot.get_chat_member(
                chat_id=config.bot.chat_id,
                user_id=user.tg_id,
            )
        except TelegramBadRequest:
            continue

        # Пользователь должен состоять в чате
        if member.status in {
            ChatMemberStatus.LEFT,
            ChatMemberStatus.KICKED,
        }:
            continue

        # В имени должен присутствовать dripary
        if "dripary" not in member.user.full_name.lower():
            continue

        winners.append(user)

        # Набрали нужное количество — заканчиваем
        if len(winners) >= giveaway.winners_count:
            break

    return winners