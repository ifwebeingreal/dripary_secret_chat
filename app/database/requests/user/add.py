from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


async def set_user(tg_id: int, first_name: str,
                   balance: int = 0,
                   rank_name: str = "Новичок", game_points: int = 0):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             first_name=first_name,
                             balance=balance,
                             rank_name=rank_name,
                             game_points=game_points))
            await session.commit()