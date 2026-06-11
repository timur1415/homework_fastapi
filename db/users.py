import aiosqlite

DB_PATH = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            nickname TEXT NOT NULL,
            bio TEXT,
            avatar TEXT DEFAULT '😊',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );""")

        await db.commit()
        print("создал таблицу users")

        await db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );""")
        await db.commit()
        # Ensure migration: add `image` column if it doesn't exist (for existing DBs)
        cursor = await db.execute("PRAGMA table_info(posts)")
        cols = await cursor.fetchall()
        col_names = [c[1] for c in cols]
        if "image" not in col_names:
            await db.execute("ALTER TABLE posts ADD COLUMN image TEXT")
            await db.commit()
            print("added image column to posts (migration)")


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
    
async def update_user(nickname: str, bio: str, avatar: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET bio = ?, avatar = ? WHERE nickname = ?",
            (bio, avatar or "😊", nickname),
        )
        await db.commit()
