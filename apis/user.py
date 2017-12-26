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

from utils.api import admin_only
from . import app
from models.user import User

# this one is intended to be the boilerplate for api

user = Blueprint('User', __name__,)


@user.route('/access_token', methods=['GET'])
@jwt_refresh_token_required
def get_access_token():
    return {'access_token': create_access_token(identity=get_current_user())}


@user.route('/refresh_token', methods=['GET'])
@jwt_refresh_token_required
def get_refresh_token():
    return {'refresh_token': create_refresh_token(identity=get_current_user())}


@user.route('/', methods=['GET'])
@jwt_required
@admin_only
@use_args({'cursor': fields.String(), 'page_size': fields.Integer()})
def get_users(args):
    return User.paginate(**args).to_dict()


@user.route('/me', methods=['GET'])
@jwt_required
def get_profile():
    user = get_current_user()
    return user.to_dict()


@user.route('/facebook', methods=['POST'])
@use_args({'fat': fields.String(required=True)})
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
def put_():
    return {}


@user.route('/', methods=['DELETE'])
def delete_():
    return {}

app.register_blueprint(user, url_prefix='/users')
