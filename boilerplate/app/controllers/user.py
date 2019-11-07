"User Controller"
from flask import abort, jsonify, request
from flask_accepts import responds, accepts
from flask_praetorian import roles_required
from flask_restplus import Namespace, Resource

from app import api, guard
from app.models import User
from app.schemas import UserSchema, UserLoginSchema

# Create a namespace and attach to main API
user_api = Namespace("User", description="User Resources")

#
# REST + Examples
#

# Attach routes to namespace


# With flask-accepts, you no longer have to manually dump on the return statement.
# You can define all the request and response expectations on the route itself.
@user_api.route("/")
@user_api.doc(security="jwt")
class UserResourceFlaskAccepts(Resource):
    @responds(schema=UserSchema(many=True), api=api)
    @roles_required("admin")
    def get(self):
        users = User.query.all()

        return users


@user_api.route("/<int:user_id>")
@user_api.doc(security="jwt")
class UserIdResourceNamespace(Resource):
    @roles_required("admin")
    def get(self, user_id: int):

        user = User.query.get(user_id)
        if not user:
            abort(404, "User was not found")

        return jsonify(UserSchema().dump(user))

