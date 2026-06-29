from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=config.database.sqlalchemy_url(),
                             echo=True)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String)
    balance: Mapped[int] = mapped_column(default=0)
    rank_name: Mapped[str] = mapped_column(String)
    game_points: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Outfit(Base):
    __tablename__ = 'outfits'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    file_id: Mapped[str] = mapped_column(String)
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    message_id: Mapped[int]


class OutfitUser(Base):
    __tablename__ = 'outfit_users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id"))
    grade: Mapped[str]


class PromoCode(Base):
    __tablename__ = 'promo_codes'

    id: Mapped[intpk]
    promo_code: Mapped[str]


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    points_count: Mapped[int]


class UserTask(Base):
    __tablename__ = 'user_tasks'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    task_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Giveaway(Base):
    __tablename__ = 'giveaways'

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    file_id: Mapped[str]


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
