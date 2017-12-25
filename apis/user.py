#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from webargs import fields
from webargs.flaskparser import use_args
from flask import Blueprint
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_current_user,
                                jwt_refresh_token_required)

from utils import json_output, output_exclude, admin_only
from . import app
from models.user import User

# this one is intended to be the boilerplate for api

user = Blueprint('User', __name__,)


@user.route('/access_token', methods=['GET'])
@jwt_refresh_token_required
@json_output
def get_refresh_token():
    return {'access_token': create_access_token(identity=get_current_user())}


@user.route('/me', methods=['GET'])
@jwt_required
@json_output
def get_profile(args):
    user = get_current_user()
    return user.to_dict()


@user.route('/facebook', methods=['POST'])
@json_output
@use_args({'fat': fields.String(required=True)})
@output_exclude(User.PUBLIC_EXCLUDE)
def connect_user_from_facebook(args):
    user = User.from_fat(args['fat'])
    if user:
        logging.debug('user from: ')
        logging.debug(user)
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        d = user.to_dict()
        d['access_token'] = access_token
        d['refresh_token'] = refresh_token
        return d


@user.route('/', methods=['PUT'])
@json_output
def put_():
    return {}


@user.route('/', methods=['DELETE'])
@json_output
def delete_():
    return {}

app.register_blueprint(user, url_prefix='/users')
