from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.admin.select import get_admins
from app.database.requests.promo_code.select import get_promo_codes
from app.database.requests.task.select import get_tasks
from app.database.requests.giveaway_result.select import get_all_giveaway_results


async def admins_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить администратора", callback_data="add_admin"))

    admins = await get_admins()
    for admin in admins:
        kb.row(InlineKeyboardButton(text=f"{admin.tg_id}", callback_data=f"admin_{admin.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_admin(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deleteadmin_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"admins"))

    return kb.as_markup()


async def outfit_panel(likes: int, dislikes: int, outfit_id: int):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text=f"🎰({likes})", callback_data=f"like_{outfit_id}"))
    kb.add(InlineKeyboardButton(text=f"🫣({dislikes})", callback_data=f"dislike_{outfit_id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_outfit_{outfit_id}"))

    return kb.as_markup()


async def promo_codes_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить промокод", callback_data="add_code"))

    codes = await get_promo_codes()
    for code in codes:
        kb.row(InlineKeyboardButton(text=f"{code.promo_code}", callback_data=f"code_{code.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_promo_code(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deletecode_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"promo_codes"))

    return kb.as_markup()


async def user_tasks():
    kb = InlineKeyboardBuilder()

    tasks = await get_tasks()

    for task in tasks:
        kb.row(InlineKeyboardButton(text=f"{task.title}", callback_data=f"usertask_{task.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"user_back"))

    return kb.as_markup()


async def tasks_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить задание", callback_data="add_task"))

    tasks = await get_tasks()
    for task in tasks:
        kb.row(InlineKeyboardButton(text=f"{task.title}", callback_data=f"task_{task.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_task(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить заголовок", callback_data=f"edit_task_title_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить описание", callback_data=f"edit_task_description_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить стоимость", callback_data=f"edit_task_price_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_task_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"all_tasks"))

    return kb.as_markup()


async def complete_task(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="💨 Готово", callback_data=f"complete_task_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"tasks"))

    return kb.as_markup()


async def check_task(task_id: int, tg_id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"accept_task_{task_id}_{tg_id}"))
    kb.row(InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_task_{task_id}_{tg_id}"))
    kb.row(InlineKeyboardButton(text="🏷️ Задание", callback_data=f"show_task_{task_id}_{tg_id}"))

    return kb.as_markup()


async def result_cb():
    kb = InlineKeyboardBuilder()

    results = await get_all_giveaway_results()

    for result in results:
        kb.row(InlineKeyboardButton(text=f"Неделя №{result.week_number}", callback_data=f"result_{result.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"user_back"))

    return kb.as_markup()
