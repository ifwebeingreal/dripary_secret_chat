from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from app.database.requests.giveaway_result.select import (
    get_all_giveaway_results,
    get_giveaway_result_by_id,
)


async def giveaways_getter(dialog_manager: DialogManager, **kwargs):
    giveaways = await get_all_giveaway_results()

    return {
        "giveaways": [
            (f"Неделя №{giveaway.week_number}", giveaway.id) for giveaway in giveaways
        ]
    }


async def giveaway_info_getter(dialog_manager: DialogManager, **kwargs):
    giveaway_id = int(dialog_manager.dialog_data.get("giveaway_id"))
    giveaway = await get_giveaway_result_by_id(giveaway_id)

    if giveaway.file_id is None:
        return {
            "title": giveaway.title,
            "description": giveaway.description,
            "created_at": giveaway.created_at,
            "winners_text": giveaway.winners_text,
        }

    file_id = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_id=giveaway.file_id)
    )

    return {
        "title": giveaway.title,
        "description": giveaway.description,
        "created_at": giveaway.created_at,
        "winners_text": giveaway.winners_text,
        "file_id": file_id,
    }
