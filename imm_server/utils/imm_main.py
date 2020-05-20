from flask import Flask, Blueprint, request, jsonify
from flask_restplus import Api, Resource, fields, Namespace, reqparse
from marshmallow import Schema, fields as ma_fields, post_load
from Request_JSON_Schema import ReqSchema
from Response_JSON_Schema import RespSchema
from jsonEncoder import ComplexEncoder
from marshmallow import EXCLUDE, ValidationError
from functools import wraps 
import os, re, json, utils, logging, subprocess

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation')
app.register_blueprint(blueprint)

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    },
}

api = Api(app, security = 'apikey',authorizations=authorizations, default="ImmunoMatch", title="immunoMatch RESTful API")
app.config['SWAGGER_UI_JSONEDITOR'] = True

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'message' : 'Token is missing.'}, 401
        if token != 'mytoken':
            return {'message' : 'Your token is wrong, wrong, wrong!!!'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated

## env setting
os.environ['PYTHONHOME'] = r"C:\Users\Jurat\AppData\Local\Programs\Python\Python37"
os.environ['PYTHONPATH'] = r"C:\Users\Jurat\AppData\Local\Programs\Python\Python37\Lib\site-packages"
os.environ['R_HOME'] = r"C:\Program Files\R\R-3.6.0"
os.environ['R_USER'] = r"C:\Users\Jurat\AppData\Local\Programs\Python\Python37\Lib\site-packages\rpy2"

## rpy2
import rpy2
import rpy2.robjects as robjects
import importlib
from immuno_score import immunomatch_ed
from rpy2.robjects.packages import importr
utils = importr('utils')
# utils.install_packages('jsonlite')
# utils.install_packages('dplyr')
# utils.install_packages('ranger')

## request body schme
# features_attr = api.model('feature', {
#     'value': fields.Integer(required=True),
#     'device': fields.String(required=True)
# })

feat_root_objs = api.model('immunomatch_ed_input', {
    'age': fields.String(),
    'gender': fields.String(required=True),
    'time': fields.Date(),
    'features': fields.List(fields.Nested(api.model('feature', {
                        'value': fields.Integer(required=True),
                        'device': fields.String(required=True)
                    }), required=True))
    })

## TODO: just test
used_features = {}
used_features['name'] = fields.String(attribute='name')
used_features['value'] = fields.Integer(attribute='value')
used_features['range_value'] = fields.List(
    fields.Integer, attribute='range_value')
used_features['range_frequency'] = fields.List(
    fields.Integer, attribute='range_frequency')
used_features['importance'] = fields.Integer(attribute='importance')
used_features_payload = api.model('feature_payload', used_features)

immEd_output = api.model('immEd_output', {
    'score': fields.Integer,
    'category': fields.String,
    'guidance': fields.String,
    'is_ready': fields.Boolean,
    'used_features': fields.Nested(used_features_payload)
})

##

##
from rpy2.robjects.packages import STAP
immunomatch_ed = STAP(immunomatch_ed, "immunomatch_ed")

ns1 = Namespace('Immunomatch Ed')
@api.route('/immunomatch_ed')
class Immunomatch_ed(Resource):
    #@api.marshal_with(a_language, envelope='the_data')
    @api.doc(security='apikey')
    @token_required
    @api.expect(feat_root_objs)
    # @api.doc(body=immEd_output)
    def post(self):
        if not request.get_json():
            return bad_request('No input data provided')
        raw_dict = request.json
        req_valid_schema = ReqSchema(unknown=EXCLUDE)
        try:
            req_valid_json = req_valid_schema.load(raw_dict)
        except ValidationError as err:
            logger.error('immunomatch_ed.post: Error: %s: %s' % (err, traceback.format_exc()))
            resp = jsonify({"error": err.messages}), 403
            return json.dumps(resp)
        input_json = req_valid_schema.dump(req_valid_json)
        input_json = json.dumps(input_json)
        imm_score = immunomatch_ed.immscore(input_json)
        res = json.loads(str(imm_score))
        res = json.dumps(res, cls= ComplexEncoder, indent=4)
        return jsonify(json.loads(res))

ns2 = Namespace('Rsession')
@api.route('/rsession')
@api.doc(description="Collect Information About The Current R Session")
class RsessionResource(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self):
        # logger.info("Rsession is getting started...")
        rscript = 'C:/Program Files/R/R-3.6.0/bin/Rscript'.replace('/', '\\')
        output = subprocess.check_output([rscript,'--vanilla','-e','sessionInfo()'])
        output = output.decode('utf-8')
        lines = output.split('\n')
        lines = [re.sub(r'\r\n', ' ', line) for line in lines]
        return {'current R session info': lines}

## logger Resource class
log_parser = reqparse.RequestParser()
log_parser.add_argument("log_type", type=str, choices=["combined", "error", "rlog"])


ns3 = Namespace('')
@api.route('/log')
class loggerResource(Resource):
    @api.doc(security='apikey')
    @token_required
    @api.expect(log_parser)
    def get(self):
        app.logger.info("This is an immunomatch ED log info message")
        app.logger.warning('testing warning log')
        app.logger.error('testing error log')
        app.logger.info('testing info log')
        ## parser instantiate
        log_args = log_parser.parse_args()
        log_type = log_args["log_type"]
        return "show error {}".format(log_type)

ns4 = Namespace('')
@api.route('/about')
class aboutResource(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self):
        name = "ImmunoMatch"
        mayor = 1
        minor = 0
        patch = 0
        return jsonify(name, mayor, minor,patch)

if __name__ == '__main__':
    # api.add_resource(Immunomatch_ed, endpoint='/immunomatch_ed')
    # api.add_resource(ListStuff, endpoint='/rsession')
    api.add_namespace(ns1)
    api.add_namespace(ns2)
    api.add_namespace(ns3)
    api.add_namespace(ns4)
    app.run(debug=True)