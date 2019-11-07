from flask import abort, jsonify, request
from flask_accepts import responds, accepts
from flask_praetorian import roles_required
from flask_restplus import Namespace, Resource

from app import api, guard
from app.models import User
from app.schemas import UserSchema, UserLoginSchema


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
