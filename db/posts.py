import aiosqlite

DB_PATH = "users.db"


async def add_post(author, content):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        await db.execute(
            "INSERT OR IGNORE INTO posts (author, content) VALUES (?, ?)",
            (author, content),
        )
        await db.commit()


async def get_post(author: str, content: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT * FROM posts ORDER BY id DESC",
        
        )

        return await cursor.fetchall()