"Iris Schema"
from dataclasses import dataclass
from datetime import datetime

from marshmallow import Schema, fields, post_load


class IrisSchema(Schema):
    sep_length = fields.Float(required=True)
    sep_width = fields.Float(required=True)
    pet_length = fields.Float(required=True)
    pet_width = fields.Float(required=True)
