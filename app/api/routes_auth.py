from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.usecases.auth import AuthUsecase


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    request: RegisterRequest,
    usecase: AuthUsecase = Depends(get_auth_usecase)
    ):
    """Регистрация нового пользователя."""

    try:
        user = await usecase.register(request.email, request.password)
        return UserPublic(id=user.id, email=user.email, role=user.role)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUsecase = Depends(get_auth_usecase)
    ):
    """Логин, возвращает JWT токен."""

    try:
        email = form.username
        password = form.password
        token = await usecase.login(email, password)
        return TokenResponse(access_token=token, token_type="bearer")
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me")
async def get_me(
    user_id: int = Depends(get_current_user_id),
    usecase: AuthUsecase = Depends(get_auth_usecase)
    ):
    """Возвращает профиль текущего авторизованного пользователя."""

    try:
        user = await usecase.get_profile(user_id)
        return UserPublic(id=user.id, email=user.email, role=user.role)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
