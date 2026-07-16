from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.outfit.add import set_outfit
from app.database.requests.outfit.select import get_outfit_by_id
from app.database.requests.outfit.update import (increment_outfit_likes, increment_outfit_dislikes,
                                                 update_outfit_message_id, decrement_outfit_likes,
                                                 decrement_outfit_dislikes)
from app.database.requests.outfit.delete import delete_outfit_by_id
from app.database.requests.admin.select import get_admin_by_tg_id
from app.database.requests.outfit_user.add import set_outfit_user
from app.database.requests.outfit_user.select import get_outfit_user
from app.database.requests.outfit_user.update import update_user_outfit_grade
from app.database.requests.user.update import update_user_balance

from config import config

from app.states import SendOutfit

outfit = Router()


@outfit.callback_query(F.data == "send_outfit")
async def send_outfit(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        "Погоди не спеши...",
        show_alert=True
    )
    # await callback.message.edit_text(
    #     "<b>Отправьте ваш аутфит:</b>",
    #     reply_markup=ikb.user_back
    # )
    #
    # await state.set_state(SendOutfit.image)


@outfit.message(SendOutfit.image)
async def check_image(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id

        outfit_id = await set_outfit(tg_id=message.from_user.id,
                                     file_id=file_id,
                                     message_id=0)

        outfit_info = await get_outfit_by_id(outfit_id)

        msg = await bot.send_photo(
            chat_id=config.bot.chat_id,
            photo=file_id,
            reply_markup=await bkb.outfit_panel(outfit_info.likes, outfit_info.dislikes, outfit_id)
        )

        await update_outfit_message_id(outfit_id, msg.message_id)

        await message.answer(
            "<b>Ваш аутфит был успешно отправлен в закрытый чат!</b>",
            reply_markup=ikb.user_back
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Аутфит должен быть изображением!</b>",
            reply_markup=ikb.user_back
        )


@outfit.callback_query(F.data.startswith("delete_outfit_"))
async def delete_outfit(callback: CallbackQuery):
    outfit_id = int(callback.data.split("_")[2])
    tg_id = callback.from_user.id
    admin = await get_admin_by_tg_id(tg_id)

    if not admin:
        await callback.answer("🔴 У вас недостаточно прав для удаления!")
        return

    await delete_outfit_by_id(outfit_id)

    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
        await callback.answer(
            "Аутфит был удален из базы!",
            show_alert=True
        )


@outfit.callback_query(F.data.startswith("like_"))
async def like(callback: CallbackQuery, bot: Bot):
    tg_id = callback.from_user.id
    outfit_id = int(callback.data.split("_")[1])

    outfit_user = await get_outfit_user(tg_id, outfit_id)

    if not outfit_user:
        await set_outfit_user(tg_id, outfit_id, "like")
        await increment_outfit_likes(outfit_id)

    else:
        if outfit_user.grade == "like":
            await callback.answer("Вы уже поставили лайк!")
            return

        if outfit_user.grade == "dislike":
            await decrement_outfit_dislikes(outfit_id)
            await increment_outfit_likes(outfit_id)

        await update_user_outfit_grade(tg_id, outfit_id, "like")

    outfit_info = await get_outfit_by_id(outfit_id)

    await bot.edit_message_reply_markup(
        chat_id=config.bot.chat_id,
        message_id=outfit_info.message_id,
        reply_markup=await bkb.outfit_panel(
            outfit_info.likes,
            outfit_info.dislikes,
            outfit_id
        )
    )

    if outfit_info.likes == 30:
        await update_user_balance(outfit_info.tg_id, 30)
        try:
            await bot.send_message(
                chat_id=outfit_info.tg_id,
                text="Ваш образ набрал 30 лайков! Зачислили вам 30 DPRY на баланс!"
            )
        except Exception as e:
            print(e)


@outfit.callback_query(F.data.startswith("dislike_"))
async def dislike(callback: CallbackQuery, bot: Bot):
    tg_id = callback.from_user.id
    outfit_id = int(callback.data.split("_")[1])

    outfit_user = await get_outfit_user(tg_id, outfit_id)

    if not outfit_user:
        await set_outfit_user(tg_id, outfit_id, "dislike")
        await increment_outfit_dislikes(outfit_id)

    else:
        if outfit_user.grade == "dislike":
            await callback.answer("Вы уже поставили дизлайк!")
            return

        if outfit_user.grade == "like":
            await decrement_outfit_likes(outfit_id)
            await increment_outfit_dislikes(outfit_id)

        await update_user_outfit_grade(tg_id, outfit_id, "dislike")

    outfit_info = await get_outfit_by_id(outfit_id)

    await bot.edit_message_reply_markup(
        chat_id=config.bot.chat_id,
        message_id=outfit_info.message_id,
        reply_markup=await bkb.outfit_panel(
            outfit_info.likes,
            outfit_info.dislikes,
            outfit_id
        )
    )