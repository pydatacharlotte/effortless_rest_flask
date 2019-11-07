""" Provide the capability to configure the app based on target environment. """
# Flask configs: https://flask.palletsprojects.com/en/1.1.x/config/
# Flask-SqlALchemy configs: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
import os
from typing import Dict


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Base config. """

    DEBUG: bool = False
    SECRET_KEY: str = "top secret"


class TestingConfig(Config):
    """ Testing config. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = "my_precious_secret_key"

    #  Exceptions are propagated rather than handled by the the app’s error handlers.
    TESTING: bool = True


class DevelopmentConfig(Config):
    """ A config to be used for development, use mocks so you don't need a DB. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my_precious_development_secret_key")


class ProductionConfig(Config):
    """ Production config. """

    # Inherits defaults from parent.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dc89aa6c-93e7-474d-a55a-b2113b25fc16")


config_by_name = dict(  # pylint: disable=invalid-name
    dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
