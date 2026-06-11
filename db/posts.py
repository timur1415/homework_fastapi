import aiosqlite

DB_PATH = "users.db"


async def add_post(author, content, image: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        if image:
            await db.execute(
                "INSERT INTO posts (author, content, image) VALUES (?, ?, ?)",
                (author, content, image),
            )
        else:
            await db.execute(
                "INSERT INTO posts (author, content) VALUES (?, ?)",
                (author, content),
            )
        await db.commit()


async def get_post():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT
                posts.id,
                posts.author,
                posts.content,
                posts.created_at,
                users.avatar,
                posts.image
            FROM posts
            LEFT JOIN users ON posts.author = users.nickname
            ORDER BY posts.id DESC
            """
        )

        return await cursor.fetchall()
