from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings
from sqlalchemy.pool import NullPool

async_engine = create_async_engine(
    settings.DB_DSN,
    poolclass=NullPool
)

session_factory = async_sessionmaker(async_engine, autoflush=True, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
