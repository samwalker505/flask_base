#! /usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.wsgi import DispatcherMiddleware
from utils.errors import InvalidType, ApiError

app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['APPLICATION_ROOT'] = '/api'
app.url_map.strict_slashes = False
jwt = JWTManager(app)
CORS(app)


def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'application/json')])
    import json
    return json.dumps({'message': 'ok'})

app.wsgi_app = DispatcherMiddleware(simple, {'/api': app.wsgi_app})


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles': user.roles, 'blocked': user.blocked}


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.key.urlsafe()


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    from google.appengine.ext import ndb
    user = ndb.Key(urlsafe=identity).get()
    return user


@app.errorhandler(InvalidType)
@app.errorhandler(ApiError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    # webargs attaches additional metadata to the `data` attribute
    exc = getattr(err, 'exc')
    if exc:
        # Get validations from the ValidationError object
        messages = exc.messages
    else:
        messages = ['Invalid request']
    return jsonify({
        'messages': messages,
    }), 422
