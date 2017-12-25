#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from webargs import fields
from webargs.flaskparser import use_args
from flask import Blueprint
from utils import json_output

from . import app

# this one is intended to be the boilerplate for api

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


@simple_page.route('/', methods=['GET'])
@json_output
def get_():
    return {}


@simple_page.route('/<pid>', methods=['GET'])
@json_output
@use_args({'per_page': fields.Int()})
def get_id(args, pid):
    return {'pid': pid,
            'args': args}


@simple_page.route('/', methods=['POST'])
@json_output
def post_():
    return {}


@simple_page.route('/', methods=['PUT'])
@json_output
def put_():
    return {}


@simple_page.route('/', methods=['DELETE'])
@json_output
def delete_():
    return {}

app.register_blueprint(simple_page, url_prefix='/pages')
