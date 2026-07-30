from aiogram import Bot
from config import config
from app.database.requests.user.select import get_users
from app.database.requests.giveaway.select import get_giveaway
from app.database.requests.user_task.select import get_random_top_user_this_week


async def send_notify_about_giveaway(bot: Bot):
    giveaway = await get_giveaway(1)

    await bot.send_photo(
        chat_id=config.bot.chat_id,
        photo=giveaway.file_id,
        caption=f"<b>{giveaway.title}</b>\n\n{giveaway.description}"
    )


async def get_giveaway_result(bot: Bot):
    giveaway = await get_giveaway(1)

    winner = await get_random_top_user_this_week()

    if not winner:
        await bot.send_message(
            chat_id=config.bot.chat_id,
            text="❌ Нет участников для подведения итогов"
        )
        return

    name, tg_id, points = winner

    # text = (
    #     f"🎉 <b>Итоги конкурса</b>\n\n"
    #     f"<b>{giveaway.title}</b>\n"
    #     f"{giveaway.description}\n\n"
    #     f"🏆 <b>Победитель:</b>\n"
    #     f"👤 {name}\n\n"
    #     # f"💎 Баллы: {points}\n\n"
    #     f"Поздравляем! 🎊"
    # )

    text = f"""Победитель испытания n недели среди дрипарей - {name}"""

    try:
        await bot.send_photo(
            chat_id=config.bot.chat_id,
            photo=giveaway.file_id,
            caption=text
        )
    except Exception:
        # если фото протухло
        await bot.send_message(
            chat_id=config.bot.chat_id,
            text=text
        )
