from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

database_url = f"sqlite+aiosqlite:///{settings.sqlite_path}"
engine = create_async_engine(database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
