#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json

from webargs import fields
from webargs.flaskparser import use_args
from flask import Blueprint
from utils import json_output

# this one is intended to be the boilerplate for api

user = Blueprint('User', __name__,)


@user.route('/', methods=['GET'])
@json_output
def get_():
    return {}


@user.route('/<pid>', methods=['GET'])
@json_output
@use_args({'per_page': fields.Int()})
def get_id(args, pid):
    return {'pid': pid,
            'args': args}


@user.route('/facebook', methods=['POST'])
@json_output
@use_args({'fat': fields.String(required=True)})
def create_user_from_facebook(args):
    from models.user import FacebookSSOMixin
    result = FacebookSSOMixin.create_from_fat(args['fat'])
    return json.dumps(result.content)


@user.route('/', methods=['PUT'])
@json_output
def put_():
    return {}


@user.route('/', methods=['DELETE'])
@json_output
def delete_():
    return {}
