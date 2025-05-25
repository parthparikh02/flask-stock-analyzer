from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=Config.RATELIMIT_STORAGE_URL,
    storage_options=Config.RATELIMIT_STORAGE_OPTIONS,
    strategy=Config.RATELIMIT_STRATEGY,
    headers_enabled=Config.RATELIMIT_HEADERS_ENABLED,
    in_memory_fallback_enabled=Config.RATELIMIT_IN_MEMORY_FALLBACK_ENABLED
)
