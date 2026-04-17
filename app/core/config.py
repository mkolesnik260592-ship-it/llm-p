from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "llm-p"
    env: str = "local"
    jwt_secret: str = "Stenka260592"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60
    sqlite_path: str = "./app.db"
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "stepfun/step-3.5-flash:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "llm-fastapi-openrouter"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
