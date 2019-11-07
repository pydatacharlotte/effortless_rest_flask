"Iris Controller"
from flask import abort, jsonify, request, current_app
from flask_accepts import responds, accepts
from flask_praetorian import roles_required
from flask_restplus import Namespace, Resource

from app import api, guard
from app.models import User
from app.services.iris_service import IrisClf

iris_api = Namespace("Iris", description="Iris API")

# Preferably this automatically goes to a data source and gets an already
# trained classifier with prediction capabilities instead of having to manually train
# the model every time the app starts up
iris_clf = IrisClf()


@iris_api.route("/train")
@iris_api.doc(security="jwt")
class IrisTrainResource(Resource):
    def get(self):
        return iris_clf.train_iris_model()


@iris_api.route("/query")
@iris_api.doc(security="jwt")
class IrisTrainResource(Resource):
    @accepts(
        dict(name="sep_length", type=float, required=True),
        dict(name="sep_width", type=float, required=True),
        dict(name="pet_length", type=float, required=True),
        dict(name="pet_width", type=float, required=True),
        api=api,
    )
    def get(self):
        X = [
            [
                request.parsed_args["sep_length"],
                request.parsed_args["sep_width"],
                request.parsed_args["pet_length"],
                request.parsed_args["pet_width"],
            ]
        ]

        return iris_clf.query_clf(X)[0]

