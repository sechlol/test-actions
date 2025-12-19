"""
Configuration schemas for the monorepo using layered env files.

This module ONLY contains Pydantic models/schemas for configuration.

Layered Configuration:
    1. .env.shared (at repo root) - DB and shared config
    2. applications/appX/.env - App-specific config

Usage in apps:
    from common_lib.config import get_settings

    settings = get_settings("app1")  # Loads .env.shared + applications/app1/.env
"""

import argparse
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

type EnvName = Literal["local", "dev", "staging", "prod"]


def find_repo_root() -> Path:
    """
    Find the repository root by looking for common markers.
    Walks up from current directory until it finds .git or pyproject.toml with [tool.poetry]
    """
    current = Path.cwd()

    # Walk up the directory tree
    for parent in [current, *current.parents]:
        # Check for .git directory
        if (parent / ".git").exists():
            return parent
        # Check for root pyproject.toml (if you have one)
        if (parent / "packages").exists() and (parent / "applications").exists():
            return parent

    # Fallback to current directory
    return current


class EnvironmentSettings(BaseSettings):
    """
    Complete settings for any application in the monorepo.

    Loads configuration in layers:
    1. Shared config from repo_root/.env.shared
    2. App-specific config from repo_root/applications/{app_name}/.env
    3. Environment variables (highest priority)
    """

    # Environment
    environment: EnvName = Field(default="local", description="Current environment")

    # App-specific settings
    app_name: str = Field(description="Application name")
    app_port: int = Field(description="Application port")
    app_host: str = Field(default="localhost", description="Application host")
    # Database settings (shared by app1 and app2)
    db_host: str = Field(default="localhost", description="Database host")
    db_port: int = Field(default=5432, description="Database port")
    db_name: str = Field(default="myapp", description="Database name")
    db_user: str = Field(default="postgres", description="Database user")
    db_password: str = Field(default="postgres", description="Database password")

    # Other Common settings
    log_level: str = Field(default="INFO", description="Log level")

    model_config = SettingsConfigDict(env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    @computed_field
    @property
    def database_url(self) -> str:
        """Construct database URL"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


def get_settings_from_env() -> EnvironmentSettings:
    """Can raise a ValidationError if some variables are not set in the environment"""
    return EnvironmentSettings()


def get_settings_from_dotenv_files_recursively(app_folder: Path, env: EnvName = "local") -> EnvironmentSettings:
    """
    Starts from the specified app folder, tries to load env files giving precedence
    to the ones next to it
    """
    for folder in app_folder.parents:
        env_path = folder / f".env.{env}"
        if env_path.exists():
            load_dotenv(str(env_path))

    return EnvironmentSettings()


def get_environment_name_from_args() -> EnvName:
    """
    Get environment value with priority:
    1. Command line argument (--env)
    2. Environment variable (ENV or ENVIRONMENT)
    3. Default to 'local'
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--env", type=str, default=None)
    args, _ = parser.parse_known_args()

    # Priority 1: Command line argument
    if args.env:
        return args.env

    # Default fallback
    return "local"
