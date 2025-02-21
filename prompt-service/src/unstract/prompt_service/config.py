import logging
from logging.config import dictConfig
from os import environ as env

from dotenv import load_dotenv
from flask import Flask
from peewee import PostgresqlDatabase
from unstract.sdk.constants import LogLevel

load_dotenv()

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

db = PostgresqlDatabase(None)


def get_env_or_die(env_key: str) -> str:
    env_value = env.get(env_key)
    if not env_value:
        raise ValueError(f"Env variable {env_key} is required")
    return env_value


def create_app() -> Flask:
    app = Flask("prompt-service")
    log_level = env.get("LOG_LEVEL", LogLevel.WARN.value)
    if log_level == LogLevel.DEBUG.value:
        app.logger.setLevel(logging.DEBUG)
    elif log_level == LogLevel.INFO.value:
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.WARNING)

    # Load required environment variables
    db_host = get_env_or_die("PG_BE_HOST")
    db_port = get_env_or_die("PG_BE_PORT")
    db_user = get_env_or_die("PG_BE_USERNAME")
    db_pass = get_env_or_die("PG_BE_PASSWORD")
    db_name = get_env_or_die("PG_BE_DATABASE")
    application_name = env.get("APPLICATION_NAME", "unstract-prompt-service")

    # Initialize and connect to the database
    db.init(
        database=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        options=f"-c application_name={application_name}",
    )
    return app
