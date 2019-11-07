"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger
from typing import List

from flask import Flask, jsonify, abort, request
from flask_accepts import accepts, responds
from flask_praetorian import Praetorian, auth_required, roles_required
from flask_restplus import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from app.schemas import UserSchema, UserSchemaWithPassword


db = SQLAlchemy()
guard = Praetorian()

authorizations = {"jwt": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api = Api(
    title="PyData Flask API",
    version="0.1.0",
    prefix="",
    doc="/docs",
    authorizations=authorizations,
)


def create_app(config_name: str) -> Flask:
    """Create the Flask application
    
    Args:
        config_name (str): Config name mapping to Config Class
    
    Returns:
        [Flask]: Flask Application
    """
    from app.config import config_by_name
    from app.models import User, Iris
    from app.controllers import user_api, iris_api, default

    # Create the app
    app = Flask(__name__)

    # Log the current config name being used and setup app with the config
    app.logger: Logger
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    # Initialize the database
    db.init_app(app)

    # Initialize Rest+ API
    api.init_app(app)
    api.add_namespace(user_api, path="/user")
    api.add_namespace(iris_api, path="/iris")

    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, User)

    return app
