from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.database.models import GiveawayResult
from app.database.requests.giveaway_result.select import get_giveaway_result_by_id

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb


giveaway_result = Router()


@giveaway_result.callback_query(F.data == "all_giveaways")
async def all_giveaways(callback: CallbackQuery):
    await callback.message.edit_text(
        "Архив с розыгрышами за всю историю <b>секретной банды:</b>",
        reply_markup=await bkb.result_cb()
    )


@giveaway_result.callback_query(F.data.startswith("result_"))
async def get_giveaway_results(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    result_id = int(callback.data.split("_")[1])
    result: GiveawayResult = await get_giveaway_result_by_id(result_id)

    try:
        await callback.message.answer_photo(
            photo=result.file_id,
            caption=f"<b>{result.title}</b>\n\n"
                    f"{result.winners_text}\n\n"
                    f"<i>Дата проведения: {result.created_at}</i>",
            reply_markup=ikb.user_back
        )
    except Exception as e:
        print(str(e))
        await callback.message.answer(
            text=f"<b>{result.title}</b>\n\n"
                    f"{result.winners_text}\n\n"
                    f"<i>Дата проведения: {result.created_at}</i>",
            reply_markup=ikb.user_back
        )