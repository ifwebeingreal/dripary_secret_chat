from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb
from app.database.requests.admin.select import get_admins

from app.database.requests.task.select import get_task_by_id
from app.database.requests.user.update import update_user_game_points
from app.database.requests.user_task.add import set_user_task
from app.database.requests.user_task.select import get_user_task

from app.states import SendScreen

task = Router()


@task.callback_query(F.data == "tasks")
async def tasks(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Задания:</b>",
        reply_markup=await bkb.user_tasks()
    )


@task.callback_query(F.data.startswith("usertask_"))
async def user_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    task = await get_task_by_id(task_id)

    await callback.message.edit_text(
        f"<b>{task.title}</b>\n\n"
        f"{task.description}\n\n"
        f"<b>Стоимость:</b> {task.points_count} Street Credits",
        reply_markup=await bkb.complete_task(task.id)
    )


@task.callback_query(F.data.startswith("complete_task_"))
async def complete_task(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    task_id = int(callback.data.split("_")[2])
    user_task = await get_user_task(tg_id, task_id)
    task = await get_task_by_id(task_id)

    if user_task:
        await callback.answer(
            "Вы уже выполнили данное задание!",
            show_alert=True
        )
        return

    if task.id == 3:
        if "#dripary" in callback.from_user.full_name.lower():
            await callback.message.edit_text(
                f"<b>Вы успешно выполнили задание!\n"
                f"Вам было начислено {task.points_count} Street Credits!</b>",
                reply_markup=ikb.user_back
            )

            await update_user_game_points(callback.from_user.id, task.points_count)
            await set_user_task(tg_id, task.id)

        else:
            await callback.answer("🚫Задание не прошло проверку 🚫", show_alert=True)

    else:
        await callback.message.edit_text(
            "<b>Отправьте скриншот выполненного задания:</b>",
            reply_markup=ikb.user_back
        )

        await state.set_state(SendScreen.screenshot)
        await state.update_data(task_id=task_id)


@task.message(SendScreen.screenshot)
async def check_screenshot(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        await state.update_data(screenshot=message.photo[-1].file_id)

        data = await state.get_data()

        tg_id = message.from_user.id
        task_id = data.get("task_id")
        screenshot = data.get("screenshot")

        admins = await get_admins()

        for admin in admins:
            await bot.send_photo(
                chat_id=admin.tg_id,
                photo=screenshot,
                caption=f"<b>Проверка выполнения</b>\n\n"
                        f"<b>Пользователь:</b> {message.from_user.full_name}",
                reply_markup=await bkb.check_task(task_id, tg_id)
            )

        await message.answer("<b>Задание было успешно отправлено на проверку!</b>",
                             reply_markup=ikb.user_back)

        await state.clear()

    else:
        await message.answer("<b>Пришлите скриншот!</b>",
                             reply_markup=ikb.user_back)

