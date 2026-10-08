"""Typed application settings.

Values come from environment variables and, when present, from the repo-root `.env`
file. Secrets are wrapped in `SecretStr` so they never appear in logs or reprs.
"""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

# src/securesoc/config.py -> parents[4] is the repository root.
_REPO_ROOT_ENV = Path(__file__).resolve().parents[4] / ".env"


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SECURESOC_",
        env_file=_REPO_ROOT_ENV,
        env_file_encoding="utf-8",
        extra="ignore",
        # Allow Settings(db_password=...) in code/tests in addition to the env aliases.
        populate_by_name=True,
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    # Database. Credentials are shared with the postgres container (POSTGRES_* names).
    db_host: str = "localhost"
    db_port: int = Field(default=5433, ge=1, le=65535)
    db_name: str = Field(
        default="securesoc", validation_alias=AliasChoices("POSTGRES_DB", "SECURESOC_DB_NAME")
    )
    db_user: str = Field(
        default="securesoc", validation_alias=AliasChoices("POSTGRES_USER", "SECURESOC_DB_USER")
    )
    db_password: SecretStr = Field(
        default=SecretStr(""),
        validation_alias=AliasChoices("POSTGRES_PASSWORD", "SECURESOC_DB_PASSWORD"),
    )
    db_connect_timeout_s: int = Field(default=3, ge=1, le=60)

    @property
    def database_url(self) -> URL:
        """SQLAlchemy URL object (keeps the password out of string formatting)."""
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.db_user,
            password=self.db_password.get_secret_value() or None,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def docs_enabled(self) -> bool:
        return self.environment != Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    return Settings()
