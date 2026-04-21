from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создаёт таблицы в базе данных при запуске приложения."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    pass

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/health")
async def get_health():
    """Проверка работоспособности сервера."""

    return {"status": "ok", "env": settings.env}
