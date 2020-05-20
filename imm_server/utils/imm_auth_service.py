import json, requests, datetime, sys, traceback
from functools import wraps
from time import time
from flask_restplus import Resource, Api, Namespace
from flask_restplus import abort, fields, inputs, reqparse
from psycopg2 import sql

from flask import Flask, request, make_response, Response, jsonify
import os, re, json, utils, logging, subprocess, psycopg2
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature

class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }
        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())
        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")
        return info['username']

'''
## to get API security key, to do:
import uuid
print(str(uuid.uuid4()))
'''
SECRET_KEY = "f4b58245-6fd4-4bce-a8a4-27ca37370a3c"
expires_in = 600
auth = AuthenticationToken(SECRET_KEY, expires_in)

app = Flask(__name__)
api = Api(app,authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="API AUTH TOKEN", 
          title="immunoMatch RESTful API", 
          description="Immunomatch ED API Authentication View") 

# db = SQLAlchemy(app)
# from sqlalchemy import create_engine
# db_engine = create_engine('postgresql://postgres:prenosis@localhost:5432/api_authen_db')

db = psycopg2.connect(database='nosis_user', user='postgres', password='solaris', host='localhost', port="5432")

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')
        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)
    return decorated

credential_model = api.model('credential', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    # 'email': fields.String(required=True)
})

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)

@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        ## db connection
        cursor = db.cursor()
        cursor.execute('SELECT * FROM public.authorized_user_table')
        users = cursor.fetchall()
        for user in users:
            if username == user[1]:
                if password == user[2]:
                    return {"token": auth.generate_token(username)}
                api.abort(401, "Wrong password")
        api.abort(404, "Username: {} doesn't exist".format(username))

    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_model, validate=True)
    def post(self):
        json_data = request.get_json(force=True)
        username = json_data['username']
        password = json_data['password']
        user = {"username": username, "password": password}
        # user = {'user_id':username,'password': password}

        insert_statement = "insert into authorized_user_table ({}) values ({})"
        cols = sql.SQL(", ").join([sql.Identifier(x) for x in user.keys()])
        vals = sql.SQL(", ").join([sql.Placeholder() for _ in user.values()])
        insert_statement = sql.SQL(insert_statement).format(cols, vals)
        try:
            cursor = db.cursor()
            cursor.execute(insert_statement, tuple(user.values()))
            db.commit()
        except: 
            tb = sys.exc_info()
            traceback.print_exception(*tb)
            db.rollback()
            return {"message": "{} has already been signed".format(username)}, 400
        return (
            {
                "message": "{} Register Successfully".format(username),
                "prediction_id": username,
            },
            200,
        )

if __name__ == '__main__':
    db = psycopg2.connect(database='nosis_user', user='postgres', password='solaris', host='localhost', port="5432")
    app.run(debug=True)
