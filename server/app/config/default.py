from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):

    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8000))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
