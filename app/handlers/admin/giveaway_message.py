import datetime

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.giveaway.select import get_giveaway, get_giveaway_winners
from app.database.requests.giveaway.update import (
    update_giveaway_file_id,
    update_giveaway_title,
    update_giveaway_description,
    update_giveaway_winners_count,
    update_giveaway_is_results_enabled,
)
from app.database.requests.giveaway_result.add import set_giveaway_result
from app.database.requests.giveaway_result.select import (
    get_giveaway_result_by_week_number,
)
from app.database.requests.giveaway_result.update import (
    update_giveaway_result_winners_text,
)

from app.states import EditGiveaway

from config import config

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


async def show_giveaway_panel(message: Message):
    giveaway_info = await get_giveaway(1)

    if giveaway_info is None:
        await message.answer("❌ Розыгрыш не найден.")
        return

    friday_time = get_next_friday_11()

    notify_status = "🟢 Включена" if giveaway_info.is_notify_enabled else "🔴 Выключена"

    results_status = (
        "🟢 Включено" if giveaway_info.is_results_enabled else "🔴 Выключено"
    )

    await message.answer_photo(
        photo=giveaway_info.file_id,
        caption=(
            "<b>🎁 Панель управления конкурсом</b>\n\n"
            f"<b>Неделя конкурса:</b> {giveaway_info.week_count}\n"
            f"<b>Заголовок:</b> {giveaway_info.title}\n"
            f"<b>Описание:</b> {giveaway_info.description}\n"
            f"<b>Количество победителей:</b> {giveaway_info.winners_count}\n"
            f"<b>Бот подведет итоги:</b> "
            f"{friday_time.strftime('%d.%m.%Y %H:%M')}\n\n"
            "<b>⚙️ Автоматизация:</b>\n"
            f"<b>Публикация розыгрыша:</b> {notify_status}\n"
            f"<b>Подведение итогов:</b> {results_status}\n\n"
            "<i>Выберите действие:</i>"
        ),
        reply_markup=ikb.giveaway_panel,
    )


@giveaway.callback_query(F.data == "giveaway")
async def giveaway_data(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await show_giveaway_panel(callback.message)


@giveaway.callback_query(F.data == "toggle_giveaway_notify")
async def toggle_giveaway_notify(callback: CallbackQuery):
    giveaway_info = await get_giveaway(1)

    if giveaway_info is None:
        await callback.answer(
            "❌ Розыгрыш не найден!",
            show_alert=True,
        )
        return

    new_status = not giveaway_info.is_notify_enabled

    await update_giveaway_is_notify_enabled(
        giveaway_id=1,
        is_notify_enabled=new_status,
    )

    await callback.answer(
        "✅ Автопубликация включена!"
        if new_status
        else "❌ Автопубликация выключена!"
    )

    await callback.message.delete()
    await show_giveaway_panel(callback.message)


@giveaway.callback_query(F.data == "toggle_giveaway_results")
async def toggle_giveaway_results(callback: CallbackQuery):
    giveaway_info = await get_giveaway(1)

    if giveaway_info is None:
        await callback.answer(
            "❌ Розыгрыш не найден!",
            show_alert=True,
        )
        return

    new_status = not giveaway_info.is_results_enabled

    await update_giveaway_is_results_enabled(
        giveaway_id=1,
        is_results_enabled=new_status,
    )

    await callback.answer(
        "✅ Автоматическое подведение итогов включено!"
        if new_status
        else "❌ Автоматическое подведение итогов выключено!"
    )

    await callback.message.delete()
    await show_giveaway_panel(callback.message)


@giveaway.callback_query(F.data == "change_giveaway_title")
async def change_giveaway_title(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новый заголовок для конкурса:</b>", reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditGiveaway.new_title)


@giveaway.message(EditGiveaway.new_title)
async def check_new_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 100:
        await update_giveaway_title(1, message.text)

        await state.clear()
        await show_giveaway_panel(message)

    else:
        await message.answer(
            "Заголовок должен быть до 100 символов!",
            reply_markup=ikb.admin_cancel,
        )


@giveaway.callback_query(F.data == "change_giveaway_description")
async def change_giveaway_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новое описание для конкурса:</b>", reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditGiveaway.new_description)


@giveaway.message(EditGiveaway.new_description)
async def check_new_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await update_giveaway_description(1, message.html_text)

        await state.clear()
        await show_giveaway_panel(message)

    else:
        await message.answer(
            "Описание должно быть до 1000 символов!",
            reply_markup=ikb.admin_cancel,
        )


@giveaway.callback_query(F.data == "change_giveaway_file_id")
async def change_giveaway_file_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новое изображение для конкурса:</b>",
        reply_markup=ikb.admin_cancel,
    )

    await state.set_state(EditGiveaway.new_file_id)


@giveaway.message(EditGiveaway.new_file_id)
async def check_new_file_id(message: Message, state: FSMContext):
    if message.photo:
        await update_giveaway_file_id(
            1,
            message.photo[-1].file_id,
        )

        await state.clear()
        await show_giveaway_panel(message)

    else:
        await message.answer(
            "Пришлите изображение!",
            reply_markup=ikb.admin_cancel,
        )


@giveaway.callback_query(F.data == "change_giveaway_winners_count")
async def change_giveaway_winners_count(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(
        "<b>Отправьте новое количество победителей для конкурса:</b>",
        reply_markup=ikb.admin_cancel,
    )

    await state.set_state(EditGiveaway.new_winners_count)


@giveaway.message(EditGiveaway.new_winners_count)
async def check_new_winners_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await update_giveaway_winners_count(
            1,
            int(message.text),
        )

        await state.clear()
        await show_giveaway_panel(message)

    else:
        await message.answer(
            "Количество должно быть больше нуля!",
            reply_markup=ikb.admin_cancel,
        )


@giveaway.callback_query(F.data == "change_giveaway_winner")
async def change_giveaway_winner(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    await callback.answer()
    await callback.message.delete()

    giveaway_info = await get_giveaway(1)

    winners = await get_giveaway_winners(
        bot=bot,
        giveaway_id=1,
    )

    if not winners:
        await callback.message.answer(
            "❌ Не удалось найти подходящих участников для розыгрыша.",
            reply_markup=ikb.admin_cancel,
        )
        return

    # Получаем актуальные данные победителей из Telegram
    winners_data = []

    for winner in winners:
        try:
            member = await bot.get_chat_member(
                chat_id=config.bot.chat_id,
                user_id=winner.tg_id,
            )

            actual_user = member.user

            username = actual_user.username
            first_name = actual_user.first_name

        except Exception as e:
            print(f"Не удалось получить актуальные данные " f"{winner.tg_id}: {e}")

            username = winner.username
            first_name = winner.first_name

        winners_data.append(
            {
                "tg_id": winner.tg_id,
                "username": username,
                "first_name": first_name,
            }
        )

    winners_text = "\n".join(
        (
            f"{i + 1}. "
            f"{'@' + user['username'] if user['username'] else user['first_name']} "
            f"(<code>{user['tg_id']}</code>)"
        )
        for i, user in enumerate(winners_data)
    )

    if len(winners) < giveaway_info.winners_count:
        warning = (
            f"\n\n⚠️ Найдено только <b>{len(winners)}</b> "
            f"из <b>{giveaway_info.winners_count}</b> "
            f"необходимых победителей."
        )
    else:
        warning = ""

    text = (
        "🏆 <b>Предварительные результаты розыгрыша</b>\n\n"
        "Случайным образом были выбраны следующие победители:\n\n"
        f"{winners_text}"
        f"{warning}\n\n"
        "Если всё верно, нажмите <b>«Подтвердить»</b> — "
        "результаты будут опубликованы в чате.\n\n"
        "Если хотите выбрать победителей заново, "
        "нажмите <b>«Перевыбрать»</b>."
    )

    # Храним не только текст, но и ID новых победителей
    await state.update_data(
        winners_text=winners_text,
        winner_ids=[winner["tg_id"] for winner in winners_data],
    )

    await callback.message.answer(
        text,
        reply_markup=ikb.check_winners,
    )

    await state.set_state(EditGiveaway.new_winners)


@giveaway.callback_query(
    F.data == "accept_winners",
    EditGiveaway.new_winners,
)
async def accept_winners(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    await callback.answer()

    data = await state.get_data()

    winners_text = data.get("winners_text")
    winner_ids = data.get("winner_ids", [])

    if not winners_text or not winner_ids:
        await callback.message.edit_text(
            "❌ Победители не были выбраны.",
            reply_markup=ikb.admin_cancel,
        )
        await state.clear()
        return

    giveaway_info = await get_giveaway(1)

    if giveaway_info is None:
        await callback.message.edit_text(
            "❌ Розыгрыш не найден.",
            reply_markup=ikb.admin_cancel,
        )
        await state.clear()
        return

    tag = f"WINNER#{giveaway_info.week_count}"

    # Получаем предыдущий результат этой недели
    result = await get_giveaway_result_by_week_number(giveaway_info.week_count)

    # Снимаем тег со СТАРЫХ победителей
    if result:
        #
        # Здесь должны получить tg_id предыдущих победителей.
        #
        # Например:
        #
        # old_winner_ids = result.winner_ids
        #
        # Если сейчас в GiveawayResult у тебя хранится только
        # winners_text, ниже объяснил, что нужно добавить.
        #

        old_winner_ids = getattr(
            result,
            "winner_ids",
            [],
        )

        for user_id in old_winner_ids:
            # Если человек снова победил,
            # снимать и заново выдавать тег нет смысла
            if user_id in winner_ids:
                continue

            try:
                await bot.set_chat_member_tag(
                    chat_id=config.bot.chat_id,
                    user_id=user_id,
                    tag="",
                )

                print(f"Тег снят с предыдущего " f"победителя {user_id}")

            except Exception as e:
                print(f"Не удалось снять тег с " f"{user_id}: {e}")

    for user_id in winner_ids:
        try:
            await bot.set_chat_member_tag(
                chat_id=config.bot.chat_id,
                user_id=user_id,
                tag=tag,
            )

            print(f"Пользователю {user_id} " f"установлен тег {tag}")

        except Exception as e:
            print(f"Не удалось установить тег " f"{user_id}: {e}")

    text = (
        f"🏆 <b>Победители испытания "
        f"{giveaway_info.week_count} недели банды</b>\n\n"
        f"{winners_text}"
    )

    try:
        await bot.send_photo(
            chat_id=config.bot.chat_id,
            photo=giveaway_info.file_id,
            caption=text,
        )

    except Exception as e:
        print(f"Не удалось отправить фото: {e}")

        await bot.send_message(
            chat_id=config.bot.chat_id,
            text=text,
        )

    if not result:
        await set_giveaway_result(
            week_number=giveaway_info.week_count,
            title=giveaway_info.title,
            description=giveaway_info.description,
            file_id=giveaway_info.file_id,
            winners_text=text,
        )

    else:
        await update_giveaway_result_winners_text(
            results_id=result.id,
            winners_text=text,
        )

    await callback.message.edit_text(
        "✅ <b>Результаты были отправлены в группу</b>",
        reply_markup=ikb.admin_cancel,
    )

    await state.clear()


@giveaway.callback_query(F.data == "send_giveaway_post_more")
async def send_giveaway_post_more(callback: CallbackQuery, bot: Bot):
    giveaway_info = await get_giveaway(1)

    await bot.send_photo(
        chat_id=config.bot.chat_id,
        photo=giveaway_info.file_id,
        caption=f"<b>{giveaway_info.title}</b>\n\n{giveaway_info.description}",
    )

    await callback.message.edit_text(
        "<b>Пост с розыгрышем был успешно отправлен в чат!</b>",
        reply_markup=ikb.admin_cancel,
    )
