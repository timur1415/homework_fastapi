from db.db import get_db_session
from db.models import User
from sqlalchemy import select


async def add_user(password, nickname, bio='', avatar='😊'):
    async with get_db_session() as session:
        user = User(nickname=nickname, password=password, bio=bio, avatar=avatar)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def get_user(id):
    async with get_db_session() as session:
        cursor = await session.execute(select(User).where(User.id == id))
        return cursor.scalars().first()


async def user_exsists(nickname):
    async with get_db_session() as session:
        cursor = await session.execute(select(User).where(User.nickname == nickname))
        user = cursor.scalar_one_or_none()
        return user is not None


async def update_user(id, bio: str, avatar: str = None):
    async with get_db_session() as session:
        cursor = await session.execute(select(User).where(User.id == id))
        user = cursor.scalar_one_or_none()
        if user is None:
            return None

        user.bio = bio
        user.avatar = avatar or "😊"
        await session.commit()
        await session.refresh(user)

        return user
    

async def get_user_by_nickname(nickname):
    async with get_db_session() as session:
        cursor = await session.execute(
            select(User).where(User.nickname == nickname)
        )
        return cursor.scalar_one_or_none()

