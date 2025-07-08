from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool 

from app.config import settings 

# Асинхронный движок
def create_engine(db_url: str):
    engine = create_async_engine(
        db_url,
        connect_args={"check_same_thread": False}, # Доступ к одному соединению из разных потоков
        poolclass=NullPool,  # Отключение пуллинга 
    )
    return engine

engine = create_engine(settings.DATABASE_URL)

# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

# База для создания моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

# Генератор сессий
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

# Создание структуры только для пустой бд
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)