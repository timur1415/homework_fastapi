from db.db import get_db_session
from db.models import Post
from sqlalchemy import select


async def add_post(author, content, image: str = None):
    async with get_db_session() as session:
        post = Post(author=author, content=content, image=image)
        session.add(post)

        await  session.commit()
        await session.refresh(post)

        return post
    

async def get_post():
    async with get_db_session() as session:
        cursor = await session.execute(
            select(Post).order_by(Post.id.desc())
        )
    return cursor.scalars().all()