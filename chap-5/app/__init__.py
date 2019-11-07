"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger
from typing import List

from flask import Flask, abort, jsonify, request
from flask_accepts import responds, accepts
from flask_praetorian import Praetorian, auth_required, roles_required
from flask_restplus import Api, Resource, Namespace, fields
from flask_sqlalchemy import SQLAlchemy

from app.schemas.user import UserSchema, UserSchemaWithPassword, UserLoginSchema

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

    # Initialize Rest+ API
    api.init_app(app)
    # Create a namespace and attach to main API
    user_api = Namespace("User", description="User Resources")
    api.add_namespace(user_api, path="/users")

    #
    # REST + Examples
    #

    # Attach routes to namespace

    @api.route("/login")
    class UserLoginResource(Resource):
        @accepts(schema=UserLoginSchema, api=api)
        @responds(dict(name="access_token", type=str), status_code=200, api=api)
        def post(self):
            # I can confidently access parsed_args based on @accepts criteria
            # use request.parsed_obj for body
            # use request.parsed_args for query params
            username = request.parsed_obj["username"]
            password = request.parsed_obj["password"]

            user = guard.authenticate(username, password)
            ret = {"access_token": guard.encode_jwt_token(user)}
            return ret

    @user_api.route("")
    @user_api.doc(security="jwt")
    class UserResourceNamespace(Resource):
        @auth_required
        def get(self):

            users = User.query.all()

            return jsonify(UserSchema(many=True).dump(users))

    @user_api.route("/admin-only")
    @user_api.doc(security="jwt")
    class UserAdminOnlyResourceNamespace(Resource):
        @roles_required("admin")
        def get(self):

            users = User.query.all()

            return jsonify(UserSchemaWithPassword(many=True).dump(users))

    @user_api.route("/<int:user_id>")
    @user_api.doc(security="jwt")
    class UserIdResourceNamespace(Resource):
        @roles_required("admin")
        def get(self, user_id: int):

            user = User.query.get(user_id)
            if not user:
                abort(404, "User was not found")

            return jsonify(UserSchema().dump(user))

    return app
