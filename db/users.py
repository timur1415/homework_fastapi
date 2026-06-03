import aiosqlite

DB_PATH = "users.db"


async def get_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        await db.commit()
        print("База готова к труду и обороне!")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            nickname TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );""")

        await db.commit()
        print("создал таблицу")


async def add_user(password: str, nickname: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        await db.execute(
            "INSERT OR IGNORE INTO users (password, nickname) VALUES (?, ?)",
            (password, nickname),
        )
        await db.commit()


async def user_exists(nickname: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id FROM users WHERE nickname = ?",
        (nickname,)
        )

        user = await cursor.fetchone()
        return user is not None
    
async def get_user(nickname: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE nickname = ?",
        (nickname,)
        )

        return await cursor.fetchone()
