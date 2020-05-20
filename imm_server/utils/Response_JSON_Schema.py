from marshmallow import Schema, fields, post_load
from marshmallow import EXCLUDE
import json
from flask import jsonify

## definition of request json body schema
class Feature:
    def __init__(self, name, value, range_value, range_frequency, importance):
        self.name = name
        self.value = value
        self.range_value = range_value
        self.range_frequency = range_frequency
        self.importance = importance

class FeatureSchema(Schema):
    value = fields.Integer()
    name = fields.Str()
    importance = fields.Integer()
    range_value = fields.List(fields.Integer)
    range_frequency = fields.List(fields.Integer)
    @post_load
    def make_feature(self, data, **kwargs):
        return Feature(**data)

class App(object):
    def __init__(self, immunoscore, risk_category, guidance, readiness_flag, features_used):
        self.immunoscore = immunoscore
        self.risk_category = risk_category
        self.guidance = guidance
        self.readiness_flag = readiness_flag
        self.features_used = features_used

class RespSchema(Schema):
    immunoscore = fields.Integer()
    risk_category = fields.Str()
    guidance = fields.Str()
    readiness_flag = fields.Boolean()
    features_used = fields.List(fields.Nested(FeatureSchema))
    @post_load
    def make_app(self, data, **kwargs):
        return App(**data)
