import argparse
import logging
import os

import uvicorn
from app1.config import APP_FOLDER
from common_lib import (EnvName, get_random_event,
                        get_settings_from_dotenv_files_recursively)
from fastapi import FastAPI


def get_environment_name() -> EnvName:
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


app = FastAPI(title="App1 API")
logger = logging.getLogger(__name__)

settings = get_settings_from_dotenv_files_recursively(app_folder=APP_FOLDER, env=get_environment_name())


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/event")
async def get_event():
    return get_random_event()


@app.get("/config")
async def get_config():
    """Debug endpoint to see config (remove in production!)"""
    return {
        "app_name": settings.app_name,
        "app_port": settings.app_port,
        "environment": settings.environment,
        "db_host": settings.db_host,
        "db_name": settings.db_name,
        # Never expose passwords in real apps!
    }


def main():
    logging.basicConfig(level=settings.log_level)
    logger.info(f"Starting {settings.app_name} on {settings.app_host}:{settings.app_port}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)


if __name__ == "__main__":
    main()
