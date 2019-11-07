"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger
from typing import List

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from app.schemas.user import UserSchema, UserSchemaWithPassword

db = SQLAlchemy()

# Application Factory
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
def create_app(config_name: str) -> Flask:
    """Create the Flask application
    
    Args:
        config_name (str): Config name mapping to Config Class
    
    Returns:
        [Flask]: Flask Application
    """
    from app.config import config_by_name
    from app.models import User

    # Create the app
    app = Flask(__name__)

    # Log the current config name being used and setup app with the config
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    # Initialize the database
    db.init_app(app)

    @app.route("/")
    def hello_world() -> str:  # pylint: disable=unused-variable

        return "Hello World!"

    # !!!!!!!ALERT!!!!!!!
    # This does not work. The users are a SQLAlchemy model that must be converted.
    # Because this route is not using flask-restplus, it will not show up in Swagger
    @app.route("/uhoh", methods=["GET"])
    def uh_oh():
        users: List[User] = User.query.all()
        print(type(users))
        print(users)
        return jsonify(users)

    # This works because Marshmallow is used to dump a Python serialized
    # object (SQLAlchemy Model)
    # Because this route is not using flask-restplus, it will not show up in Swagger
    @app.route("/marsh", methods=["GET"])
    def marsh():

        users = User.query.all()

        return jsonify(UserSchema(many=True).dump(users))

    return app
