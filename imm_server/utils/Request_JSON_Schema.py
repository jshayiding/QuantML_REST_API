from marshmallow import Schema, fields, post_load
from marshmallow import EXCLUDE
import json
from flask import jsonify

## definition of request json body schema
class Feature(object):
    def __init__(self, value, device):
        self.value = value
        self.device = device
    def __repr__(self):
        return '{} is value. {} is device'.format(self.value, self.device)

class FeatureSchema(Schema):
    value = fields.Integer()
    device = fields.Str()
    @post_load
    def make_feature(self, data, **kwargs):
        return Feature(**data)

class App(object):
    def __init__(self, age, gender, PCT, IL6, CRP):
        self.age = age
        self.gender = gender
        self.PCT = PCT
        self.CRP = CRP
        self.IL6 = IL6
class ReqSchema(Schema):
    age = fields.Integer()
    gender = fields.Str()
    PCT = fields.Nested(FeatureSchema)
    CRP = fields.Nested(FeatureSchema)
    IL6 = fields.Nested(FeatureSchema)
    @post_load
    def make_app(self, data, **kwargs):
        return App(**data)