from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUsecase
from app.usecases.chat import ChatUsecase
from app.core.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_chat_repository(db: AsyncSession = Depends(get_db)) -> ChatMessagesRepository:
    return ChatMessagesRepository(db)


async def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> AuthUsecase:
    return AuthUsecase(user_repo)


async def get_chat_usecase(
        chat_repo: ChatMessagesRepository = Depends(get_chat_repository),
        openrouter_client: OpenRouterClient = Depends(get_openrouter_client)
        ) -> ChatUsecase:
    return ChatUsecase(chat_repo, openrouter_client)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return int(user_id)
