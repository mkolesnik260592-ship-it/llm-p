from app.db.models import User
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.users import UserRepository


class AuthUsecase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    async def register(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if user:
            raise ConflictError("User with this email already exists")
        else:
            hashed_pswd = hash_password(password)
            return await self.user_repository.create(email=email, password_hash=hashed_pswd)


    async def login(self, email: str, password: str) -> str:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UnauthorizedError("User with this email not found")
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Wrong password")
        return create_access_token(data={"sub": user.id})


    async def get_profile(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
