#! /usr/bin/env python
# -*- coding: utf-8 -*-
from . import app, json


@app.route('/', methods=['GET'])
@json
def get_():
    return {}


@app.route('/', methods=['POST'])
@json
def post_():
    return {}


@app.route('/', methods=['PUT'])
@json
def put_():
    return {}


@app.route('/', methods=['DELETE'])
@json
def delete_():
    return {}
