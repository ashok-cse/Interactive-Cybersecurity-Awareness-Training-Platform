"""Application configuration classes."""
import os
from datetime import timedelta


def _env_bool(name, default=False):
    """Read an environment variable as a boolean (accepts 1/true/yes/on)."""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ('1', 'true', 'yes', 'on')


# Instance/default sqlite path lives next to the project (instance folder).
_BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
_INSTANCE_DB = os.path.join(_BASE_DIR, 'instance', 'cyberaware.db')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///' + _INSTANCE_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = _env_bool('SESSION_COOKIE_SECURE', False)

    SESSION_TIMEOUT_MINUTES = int(os.environ.get('SESSION_TIMEOUT_MINUTES', 30))
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=SESSION_TIMEOUT_MINUTES)

    WTF_CSRF_ENABLED = True
    PASS_THRESHOLD = 70


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    RATELIMIT_ENABLED = False


_CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config(name=None):
    """Resolve a config class by name, env FLASK_ENV / CONFIG, or default."""
    if name is None:
        name = os.environ.get('CONFIG') or os.environ.get('FLASK_ENV') or 'default'
    return _CONFIG_MAP.get(name, DevelopmentConfig)
