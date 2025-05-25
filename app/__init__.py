import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from .config import Config, config_manager

from .extensions import db, migrate, login_manager, limiter
from .utils.constants import HttpStatusCode
from .utils.common import send_json_response

from .celery_tasks.config import make_celery

celery_app = None


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

    initialise_celery(app)

    initialise_swagger(app)

    # Register rate limit error handler
    @app.errorhandler(429)
    def ratelimit_handler(request_limit):
        limit_string = request_limit.limit.limit
        time_limit = str(limit_string).split('per')[1]
        return send_json_response(
            response_status=False,
            message_key="Request limit reached: Please try after {0}s".format(time_limit),
            http_status=HttpStatusCode.TOO_MANY_REQUESTS.value
        )

    return app


def initialise_celery(app):
    global celery_app
    celery_app = make_celery(app)

    from app.celery_tasks import tasks

    from celery.schedules import crontab

    celery_app.conf.update({
        'CELERYBEAT_SCHEDULE': {
            'fetch-nifty-daily': {
                'task': 'tasks.fetch_and_store_task',
                'schedule': crontab(minute=0, hour=0),  # Run at 12 AM every day
            },
        }
    })


def initialise_flask_login(app):
    login_manager.login_view = "v1.login"
    login_manager.init_app(app)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)


def register_blueprints(app):
    from app.views import v1_blueprint

    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")


def load_logs(app):
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


def initialise_swagger(app):
    from flasgger import Swagger

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/api/v1/docs/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/",
        "swagger_ui_oauth2": {},
        "swagger_ui_config": {
            "tryItOutEnabled": True,
            "docExpansion": "none",
        }
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Flask Stock Analyzer API",
            "description": "A RESTful API to analyze and track stock data with user authentication.",
            "contact": {
                "name": "Parth Parikh",
                "email": "parthparikh02@gmail.com",
            },
            "version": "1.0.0"
        },
        "basePath": "/api/v1",
        "schemes": [
            "http",
        ],
        "securityDefinitions": {
            "cookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "session",
                "description": "Session cookie for logged-in users"
            }
        },
        "security": [
            {"cookieAuth": []}
        ]
    }

    Swagger(app, config=swagger_config, template=swagger_template)
