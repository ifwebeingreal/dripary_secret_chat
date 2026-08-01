from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    tg_id = State()


class SendAll(StatesGroup):
    text = State()


class SendOutfit(StatesGroup):
    image = State()


class AddPromoCode(StatesGroup):
    promo_code = State()


class AddTask(StatesGroup):
    title = State()
    description = State()
    points_count = State()


class EditTask(StatesGroup):
    new_title = State()
    new_description = State()
    new_points_count = State()


class SendScreen(StatesGroup):
    screenshot = State()


class EditGiveaway(StatesGroup):
    new_title = State()
    new_description = State()
    new_file_id = State()
    new_winners_count = State()