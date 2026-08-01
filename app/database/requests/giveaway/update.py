from app.database.models import async_session
from app.database.models import Giveaway
from sqlalchemy import update


async def update_giveaway_title(id: int, title: str):
    async with async_session() as session:
        await session.execute(
            update(Giveaway).where(Giveaway.id == id).values(title=title)
        )
        await session.commit()


async def update_giveaway_description(id: int, description: str):
    async with async_session() as session:
        await session.execute(
            update(Giveaway).where(Giveaway.id == id).values(description=description)
        )
        await session.commit()


async def update_giveaway_file_id(id: int, file_id: str):
    async with async_session() as session:
        await session.execute(
            update(Giveaway).where(Giveaway.id == id).values(file_id=file_id)
        )
        await session.commit()


async def update_giveaway_winners_count(id: int, winners_count: int):
    async with async_session() as session:
        await session.execute(
            update(Giveaway).where(Giveaway.id == id).values(winners_count=winners_count)
        )
        await session.commit()