import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as aioredis

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.filters.admin_filter import AdminProtect
from app.filters.member_filter import MemberProtect

from config import config

from app.handlers.user.user_message import user
from app.handlers.user.chat_message import chat
from app.handlers.user.outfit_message import outfit
from app.handlers.user.task_message import task as user_task

from app.handlers.admin.admin_message import admin
from app.handlers.admin.promo_code_message import promo_code
from app.handlers.admin.task_message import task as admin_task
from app.handlers.admin.giveaway_message import giveaway

from app.database.models import create_db

from app.utils.giveaway_schedule.schedule import send_notify_about_giveaway, get_giveaway_result

scheduler = AsyncIOScheduler()


async def main():
    print("Bot is starting...")

    redis = await aioredis.from_url(config.redis.redis_url)
    await create_db()

    bot = Bot(token=config.bot.bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(redis))

    # dp.message.middleware(CheckSubscription())
    # dp.callback_query.middleware(CheckSubscriptionCallback())

    admin.message.middleware(AdminProtect())
    admin.callback_query.middleware(AdminProtect())
    promo_code.message.middleware(AdminProtect())
    promo_code.callback_query.middleware(AdminProtect())
    admin_task.message.middleware(AdminProtect())
    admin_task.callback_query.middleware(AdminProtect())
    giveaway.message.middleware(AdminProtect())
    giveaway.callback_query.middleware(AdminProtect())

    outfit.message.middleware(MemberProtect())
    outfit.callback_query.middleware(MemberProtect())
    user.message.middleware(MemberProtect())
    user.callback_query.middleware(MemberProtect())
    user_task.message.middleware(MemberProtect())
    user_task.callback_query.middleware(MemberProtect())

    dp.include_router(user)
    dp.include_router(admin)
    # dp.include_router(chat)
    dp.include_router(outfit)
    dp.include_router(promo_code)
    dp.include_router(admin_task)
    dp.include_router(user_task)
    dp.include_router(giveaway)

    scheduler.add_job(
        send_notify_about_giveaway,
        trigger='cron',
        day_of_week='mon',
        hour=11,
        minute=0,
        kwargs={'bot': bot}
    )
    scheduler.add_job(
        get_giveaway_result,
        trigger='cron',
        day_of_week='fri',
        hour=11,
        minute=0,
        kwargs={'bot': bot}
    )

    # scheduler.add_job(get_giveaway_result, 'interval', seconds=10, kwargs={'bot': bot})

    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
