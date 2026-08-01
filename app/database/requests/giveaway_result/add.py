from app.database.models import async_session
from app.database.models import GiveawayResult


async def set_giveaway_result(
        week_number: int,
        winners_text: str,
        title: str | None = None,
        description: str | None = None,
        file_id: str | None = None,
):
    async with async_session() as session:
        session.add(GiveawayResult(week_number=week_number,
                                   title=title,
                                   description=description,
                                   file_id=file_id,
                                   winners_text=winners_text))
        await session.commit()