import os
from configparser import ConfigParser

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

config: ConfigParser = ConfigParser()
config.read("app.conf")
base_url: str = os.environ.get("BASE_URL") or config["URLS"]["DEFAULT_BASE_URL"]

db: SQLAlchemy = SQLAlchemy()


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_URI"
    ) or os.path.expandvars(config["URLS"]["DB_URI"])
    db.init_app(app)
    Migrate(app, db)
    from src.model import character

    return app
