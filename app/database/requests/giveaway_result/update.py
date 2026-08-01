from app.database.models import async_session
from app.database.models import GiveawayResult
from sqlalchemy import update


async def update_giveaway_result_winners_text(results_id: int, winners_text: str):
    async with async_session() as session:
        await session.execute(
            update(GiveawayResult)
            .where(GiveawayResult.id == results_id)
            .values(winners_text=winners_text)
        )