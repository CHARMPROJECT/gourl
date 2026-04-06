from .database import session_factory, Base, async_engine
from database.models import *
from sqlalchemy import select, delete

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_url(uid: str):
    async with session_factory() as session:
        async with session.begin():
            url = await session.execute(select(Url).where(Url.uid == uid))
            url = url.scalar_one_or_none()
            session.expunge_all()

    return url

async def get_url_by_code(code: str):
    async with session_factory() as session:
        async with session.begin():
            url = await session.execute(select(Url).where(Url.code == code))
            url = url.scalar_one_or_none()
            session.expunge_all()

    return url

async def create_url(target_url: str):
    async with session_factory() as session:
        async with session.begin():
            url = Url(url=target_url)
            session.add(url)
            await session.commit()
            session.expunge_all()

    return url
