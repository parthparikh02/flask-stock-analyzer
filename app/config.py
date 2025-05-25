import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Celery configuration
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    CELERY_TIMEZONE = os.environ.get("CELERY_TIMEZONE", "Asia/Kolkata")
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"

    # Flask-Limiter configuration
    RATELIMIT_STORAGE_URL = os.environ.get("RATELIMIT_STORAGE_URL", "memory://")
    RATELIMIT_STRATEGY = os.environ.get("RATELIMIT_STRATEGY", "fixed-window")
    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "1 per minute")
    RATELIMIT_HEADERS_ENABLED = os.environ.get("RATELIMIT_HEADERS_ENABLED", "True").lower() == "true"
    RATELIMIT_STORAGE_OPTIONS = {}
    RATELIMIT_IN_MEMORY_FALLBACK_ENABLED = os.environ.get("RATELIMIT_IN_MEMORY_FALLBACK_ENABLED", "True").lower() == "true"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URI")


config_manager = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}