"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger
from typing import List

from flask import Flask, abort, jsonify, request
from flask_praetorian import Praetorian, auth_required, roles_required
from flask_sqlalchemy import SQLAlchemy

from app.schemas.user import UserSchema, UserSchemaWithPassword

db = SQLAlchemy()
guard = Praetorian()


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

    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, User)

    @app.route("/")
    def hello_world() -> str:  # pylint: disable=unused-variable

        return "Hello World!"

    @app.route("/login", methods=["POST"])
    def login():
        # Ignore the mimetype and always try to parse JSON.
        req = request.get_json(force=True)

        username = req.get("username", None)
        password = req.get("password", None)

        user = guard.authenticate(username, password)
        ret = {"access_token": guard.encode_jwt_token(user)}
        return (jsonify(ret), 200)

    @app.route("/users", methods=["GET"])
    @auth_required
    def users():

        users = User.query.all()

        return jsonify(UserSchema(many=True).dump(users))

    @app.route("/users/admin-only", methods=["GET"])
    @roles_required("admin")
    def users_admin():

        users = User.query.all()

        return jsonify(UserSchemaWithPassword(many=True).dump(users))

    return app
