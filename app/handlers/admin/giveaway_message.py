import datetime

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.giveaway.select import get_giveaway
from app.database.requests.giveaway.update import (update_giveaway_file_id, update_giveaway_title,
                                                   update_giveaway_description, update_giveaway_winners_count)

from app.states import EditGiveaway


giveaway = Router()


def get_next_friday_11():
    now = datetime.datetime.now()

    # 0 = понедельник ... 4 = пятница
    days_ahead = 4 - now.weekday()

    if days_ahead < 0:
        days_ahead += 7

    friday = now + datetime.timedelta(days=days_ahead)
    friday_11 = friday.replace(hour=11, minute=0, second=0, microsecond=0)

    # если уже позже пятницы 11:00 → следующая неделя
    if now >= friday_11:
        friday_11 += datetime.timedelta(days=7)

    return friday_11


@giveaway.callback_query(F.data == "giveaway")
async def giveaway_data(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    giveaway_info = await get_giveaway(1)
    friday_time = get_next_friday_11()

    await callback.message.answer_photo(
        photo=giveaway_info.file_id,
        caption=f"<b>Панель управления конкурсом</b>\n\n"
                f"<b>Заголовок:</b> {giveaway_info.title}\n"
                f"<b>Описание:</b> {giveaway_info.description}\n"
                f"<b>Количество победителей:</b> {giveaway_info.winners_count}\n"
                f"<b>Бот подведет итоги:</b> {friday_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                f"<i>Выберите действие:</i>",
        reply_markup=ikb.giveaway_panel
    )


@giveaway.callback_query(F.data == "change_giveaway_title")
async def change_giveaway_title(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новый заголовок для конкурса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditGiveaway.new_title)


@giveaway.message(EditGiveaway.new_title)
async def check_new_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 100:
        await update_giveaway_title(1, message.text)

        giveaway_info = await get_giveaway(1)
        friday_time = get_next_friday_11()

        await message.answer_photo(
            photo=giveaway_info.file_id,
            caption=f"<b>Панель управления конкурсом</b>\n\n"
                    f"<b>Заголовок:</b> {giveaway_info.title}\n"
                    f"<b>Описание:</b> {giveaway_info.description}\n"
                    f"<b>Количество победителей:</b> {giveaway_info.winners_count}\n"
                    f"<b>Бот подведет итоги:</b> {friday_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=ikb.giveaway_panel
        )

        await state.clear()

    else:
        await message.answer("Заголовок должен быть до 100 символов!",
                             reply_markup=ikb.admin_cancel)


@giveaway.callback_query(F.data == "change_giveaway_description")
async def change_giveaway_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новое описание для конкурса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditGiveaway.new_description)


@giveaway.message(EditGiveaway.new_description)
async def check_new_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await update_giveaway_description(1, message.html_text)

        giveaway_info = await get_giveaway(1)
        friday_time = get_next_friday_11()

        await message.answer_photo(
            photo=giveaway_info.file_id,
            caption=f"<b>Панель управления конкурсом</b>\n\n"
                    f"<b>Заголовок:</b> {giveaway_info.title}\n"
                    f"<b>Описание:</b> {giveaway_info.description}\n"
                    f"<b>Количество победителей:</b> {giveaway_info.winners_count}\n"
                    f"<b>Бот подведет итоги:</b> {friday_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=ikb.giveaway_panel
        )

        await state.clear()

    else:
        await message.answer("Описание должно быть до 1000 символов!",
                             reply_markup=ikb.admin_cancel)


@giveaway.callback_query(F.data == "change_giveaway_file_id")
async def change_giveaway_file_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новое изображение для конкурса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditGiveaway.new_file_id)


@giveaway.message(EditGiveaway.new_file_id)
async def check_new_file_id(message: Message, state: FSMContext):
    if message.photo:
        await update_giveaway_file_id(1, message.photo[-1].file_id)

        giveaway_info = await get_giveaway(1)
        friday_time = get_next_friday_11()

        await message.answer_photo(
            photo=giveaway_info.file_id,
            caption=f"<b>Панель управления конкурсом</b>\n\n"
                    f"<b>Заголовок:</b> {giveaway_info.title}\n"
                    f"<b>Описание:</b> {giveaway_info.description}\n"
                    f"<b>Количество победителей:</b> {giveaway_info.winners_count}\n"
                    f"<b>Бот подведет итоги:</b> {friday_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=ikb.giveaway_panel
        )

        await state.clear()

    else:
        await message.answer("Пришлите изображение!",
                             reply_markup=ikb.admin_cancel)


@giveaway.callback_query(F.data == "change_giveaway_winners_count")
async def change_giveaway_winners_count(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новое количество победителей для конкурса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditGiveaway.new_winners_count)


@giveaway.message(EditGiveaway.new_winners_count)
async def check_new_winners_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await update_giveaway_winners_count(1, int(message.text))

        giveaway_info = await get_giveaway(1)
        friday_time = get_next_friday_11()

        await message.answer_photo(
            photo=giveaway_info.file_id,
            caption=f"<b>Панель управления конкурсом</b>\n\n"
                    f"<b>Заголовок:</b> {giveaway_info.title}\n"
                    f"<b>Описание:</b> {giveaway_info.description}\n"
                    f"<b>Количество победителей:</b> {giveaway_info.winners_count}\n"
                    f"<b>Бот подведет итоги:</b> {friday_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=ikb.giveaway_panel
        )

        await state.clear()

    else:
        await message.answer("Количество должно быть больше нуля!",
                             reply_markup=ikb.admin_cancel)