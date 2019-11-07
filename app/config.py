""" Provide the capability to configure the app based on target environment. """
# Flask configs: https://flask.palletsprojects.com/en/1.1.x/config/
# Flask-SqlALchemy configs: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# Flask-Praetorian configs: https://flask-praetorian.readthedocs.io/en/latest/notes.html#configuration-settings
import os
from typing import Dict


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Base config. """

    DEBUG: bool = False
    SECRET_KEY: str = "top secret"

    # Tracks modifications of objects and emit signals
    # This requires extra memory and should be disabled if not needed.
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # JWT Configs
    # The default length of time that a JWT may be used to access a protected endpoint
    JWT_ACCESS_LIFESPAN: Dict[str, int] = {"hours": 24}
    # The default length of time that a JWT may be refreshed. JWT may also not be
    # refreshed if its access lifespan is not expired.
    JWT_REFRESH_LIFESPAN: Dict[str, int] = {"days": 30}

    RESTPLUS_MASK_SWAGGER: bool = False


class TestingConfig(Config):
    """ Testing config. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = "my_precious_secret_key"

    #  Exceptions are propagated rather than handled by the the app’s error handlers.
    TESTING: bool = True

    # SQLAlchemy Connection string
    # use a local sqlite db for testing
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{BASEDIR}/app-test.db"


class DevelopmentConfig(Config):
    """ A config to be used for development, use mocks so you don't need a DB. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my_precious_development_secret_key")

    # SQLAlchemy Connection string
    # use provided ENV variable connection string
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL


class ProductionConfig(Config):
    """ Production config. """

    # Inherits defaults from parent.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dc89aa6c-93e7-474d-a55a-b2113b25fc16")

    # SQLAlchemy Connection string
    # use provided ENV variable connection string
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL


config_by_name = dict(  # pylint: disable=invalid-name
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
