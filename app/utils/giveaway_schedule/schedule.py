from aiogram import Bot
from config import config
from app.database.requests.user.select import get_users
from app.database.requests.admin.select import get_admins
from app.database.requests.giveaway.select import get_giveaway, get_giveaway_winners
from app.database.requests.giveaway.update import increment_giveaway_week_count
from app.database.requests.user_task.select import get_random_top_user_this_week
from app.database.requests.giveaway_result.add import set_giveaway_result


async def send_notify_about_giveaway(bot: Bot):
    giveaway = await get_giveaway(1)

    await bot.send_photo(
        chat_id=config.bot.chat_id,
        photo=giveaway.file_id,
        caption=f"<b>{giveaway.title}</b>\n\n{giveaway.description}"
    )


async def get_giveaway_result(bot: Bot):
    giveaway = await get_giveaway(1)

    winners = await get_giveaway_winners(1)

    winners_text = "\n".join(
        f"{i + 1}. @{user.username or user.first_name} (<code>{user.tg_id}</code>)"
        for i, user in enumerate(winners)
    )

    if not winners_text:
        await bot.send_message(
            chat_id=config.bot.chat_id,
            text="❌ Нет участников для подведения итогов"
        )
        return

    # name, tg_id, points = winner

    # text = (
    #     f"🎉 <b>Итоги конкурса</b>\n\n"
    #     f"<b>{giveaway.title}</b>\n"
    #     f"{giveaway.description}\n\n"
    #     f"🏆 <b>Победитель:</b>\n"
    #     f"👤 {name}\n\n"
    #     # f"💎 Баллы: {points}\n\n"
    #     f"Поздравляем! 🎊"
    # )

    text = f"Победитель испытания {giveaway.week_count} недели среди дрипарей\n\n{winners_text}"

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

    await set_giveaway_result(
        title=giveaway.title,
        description=giveaway.description,
        file_id=giveaway.file_id,
        week_number=giveaway.week_count,
        winners_text=text
    )


async def new_giveaway_week(bot: Bot):
    admins = await get_admins()
    await increment_giveaway_week_count(1)
    giveaway = await get_giveaway(1)

    for admin in admins:
        await bot.send_message(
            chat_id=admin.tg_id,
            text=f"<b>Неделя конкурса была обновлена!</b>\n\n"
                 f"<b>Текущая неделя:</b> {giveaway.week_count}\n"
        )
