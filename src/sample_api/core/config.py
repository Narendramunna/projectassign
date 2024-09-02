import os
from typing import Any, Optional, Union

from pydantic import field_validator, PostgresDsn
from pydantic_settings import BaseSettings
from pydantic_core.core_schema import FieldValidationInfo


class Settings(BaseSettings):

    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: list[str] = os.getenv(
        "ORIGINS", "http://localhost*").split(",")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_HOST", "127.0.0.1:5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = PostgresDsn.build(
        scheme="postgresql",
        username=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "127.0.0.1:5432"),
        path=os.getenv('POSTGRES_DB', 'postgres')
    )


@field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
@classmethod
def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
    if isinstance(v, str):
        return v
    return PostgresDsn.build(
        scheme="postgresql+psycopg2",
        username=info.data.get("POSTGRES_USER"),
        password=info.data.get("POSTGRES_PASSWORD"),
        host=info.data.get("POSTGRES_HOST"),
        path=info.data.get("POSTGRES_DB") or "",
    )


Configuration = Settings()
