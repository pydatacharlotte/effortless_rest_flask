"User Schema"
from dataclasses import dataclass
from datetime import datetime

from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    user_id = fields.Integer()
    username = fields.String(required=True)
    roles = fields.String()
    is_active = fields.Boolean()
    created_datetime = fields.DateTime()


class UserSchemaWithPassword(UserSchema):
    password = fields.String(required=True)


class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
