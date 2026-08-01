from app.database.models import async_session
from app.database.models import GiveawayResult
from sqlalchemy import select


async def get_all_giveaway_results():
    async with async_session() as session:
        results = await session.scalars(select(GiveawayResult))
        return results


async def get_giveaway_result_by_id(giveaway_result_id: int):
    async with async_session() as session:
        result = await session.scalar(
            select(GiveawayResult).where(GiveawayResult.id == giveaway_result_id)
        )
        return result


async def get_giveaway_result_by_week_number(week_number: int):
    async with async_session() as session:
        result = await session.scalar(
            select(GiveawayResult).where(
                GiveawayResult.week_number == week_number
            )
        )
        return result