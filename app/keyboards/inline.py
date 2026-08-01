from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассылка", callback_data="sender")],
        [InlineKeyboardButton(text="Розыгрыш", callback_data="giveaway")],
        [InlineKeyboardButton(text="Администраторы", callback_data="admins")],
        [InlineKeyboardButton(text="Промокоды", callback_data="promo_codes")],
        [InlineKeyboardButton(text="Задания", callback_data="all_tasks")],
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

user_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Задания", callback_data="tasks")],
        [InlineKeyboardButton(text="Отправить аутфит", callback_data="send_outfit")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Поддержка", url="https://t.me/dripary_bot")],
    ]
)

to_bot = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получать кредитсы", url="https://t.me/dripcommittee_bot")]
    ]
)

profile_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить промокод", callback_data="code_info")],
        [InlineKeyboardButton(text="Назад", callback_data="user_back")],
    ]
)

get_code = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить", callback_data="get_code")],
        [InlineKeyboardButton(text="Назад", callback_data="user_back")],
    ]
)

user_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="user_back")],
    ]
)

close = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close")],
    ]
)

giveaway_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Выбрать победителя", callback_data="change_giveaway_winner")],
        [InlineKeyboardButton(text="✏️ Изменить заголовок", callback_data="change_giveaway_title")],
        [InlineKeyboardButton(text="✏️ Изменить описание", callback_data="change_giveaway_description")],
        [InlineKeyboardButton(text="✏️ Изменить изображение", callback_data="change_giveaway_file_id")],
        [InlineKeyboardButton(text="✏️ Изменить кол-во", callback_data="change_giveaway_winners_count")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")],
    ]
)

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url=config.bot.channel_link)],
        [InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]
    ]
)
