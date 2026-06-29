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

from config import config

from app.filters.chat_type import ChatTypeFilter

user = Router()


# @user.message(F.photo)
# async def get_photo_id(message: Message):
#     photo_id = message.photo[-1].file_id
#     await message.answer(photo_id)


@user.message(F.new_chat_members)
async def user_joined(message: Message):
    if message.chat.id != config.bot.chat_id:
        return

    await message.answer(
        text=f"@{message.from_user.username} - новый дрипарь в нашем чате!\n"
             f"Поприветствуем!",
        reply_markup=ikb.to_bot
    )

    await set_user(message.from_user.id, message.from_user.full_name)


@user.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    await callback.message.edit_text("Спасибо за подписку, вы можете пользоваться ботом!")

    await set_user(callback.from_user.id, callback.from_user.full_name)


@user.message(CommandStart(), ChatTypeFilter("private"))
async def start_command(message: Message):
    await set_user(message.from_user.id, message.from_user.full_name)

    await message.answer("Добро пожаловать!",
                         reply_markup=ikb.user_panel)

    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == message.from_user.id:
            await message.answer(f"Вы успешно авторизовались как администратор!",
                                 reply_markup=rkb.admin_menu)
            return


@user.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user_info = await get_user(tg_id)

    await callback.message.edit_text(
        f"<b>Профиль пользователя</b>\n\n"
        f"<b>Имя:</b> {callback.from_user.full_name}\n"
        f"<b>Баланс:</b> {user_info.balance} DRPY\n"
        f"<b>Ранг:</b> {user_info.rank_name}\n\n"
        f"<b>Ты с нами с {user_info.date}!</b>",
        reply_markup=ikb.profile_panel
    )


@user.callback_query(F.data == "code_info")
async def code_info(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user_info = await get_user(tg_id)

    await callback.message.edit_text(
        f"<b>Для того, чтобы получить промокод, нужно 100 кердитсов</b>\n\n"
        f"<b>Ваш баланс:</b> <code>{user_info.balance} DPRY</code>\n\n"
        f"<i>*Для повышения кредтсов выполняй задания</i>",
        reply_markup=ikb.get_code
    )


@user.callback_query(F.data == "get_code")
async def get_code(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user_info = await get_user(tg_id)

    if user_info.balance < 100:
        await callback.answer(
            "На вашем счету недостаточно DRPY!",
            show_alert=True
        )
        return



@user.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Добро пожаловать!",
        reply_markup=ikb.user_panel
    )

    await state.clear()