from app.database.models import async_session, User, Admin
from app.database.models import Giveaway
from sqlalchemy import select, func


async def get_giveaway(id: int):
    async with async_session() as session:
        giveaway = await session.scalar(
            select(Giveaway)
            .where(Giveaway.id == id)
        )
        return giveaway



async def get_giveaway_winners(giveaway_id: int) -> list[User]:
    async with async_session() as session:
        giveaway = await session.get(Giveaway, giveaway_id)

        if giveaway is None:
            return []

        admin_ids = select(Admin.tg_id)

        stmt = (
            select(User)
            .where(User.tg_id.not_in(admin_ids))
            .order_by(func.random())
            .limit(giveaway.winners_count)
        )

        result = await session.execute(stmt)

        return result.scalars().all()