import logging
from logging.handlers import RotatingFileHandler
import os


from flask import Flask
from .config import Config, config_manager

from .extensions import db, migrate, login_manager



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_manager[config_name])

    config_manager[config_name].init_app(app)
    
    register_extensions(app)

    initialise_flask_login(app)
    
    from app import models

    register_blueprints(app)

    if not app.debug and not app.testing:
        load_logs(app)

    return app

def initialise_flask_login(app):
    login_manager.login_view = "v1.login"
    login_manager.init_app(app)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from app.views import v1_blueprint

    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")

def load_logs(app):
    if app.config["LOG_TO_STDOUT"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("app startup")
    return