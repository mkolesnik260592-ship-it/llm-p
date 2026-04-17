from pydantic import BaseModel


class UserPublic(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True
