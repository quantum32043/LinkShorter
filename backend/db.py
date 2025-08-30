import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import dotenv

dotenv.load_dotenv()

engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("POSTGRES_DB")}"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with new_session() as session:
        yield session
