from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://admin:3204quant2043@localhost:5432/shorter_db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with new_session() as session:
        yield session
