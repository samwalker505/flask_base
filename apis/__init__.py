#! /usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from flask import Flask, jsonify
from utils.errors import InvalidType


app = Flask(__name__)
app.debug = True


def json(func):
    @wraps(func)
    def _func(*args, **kwds):
        result = func(*args, **kwds)
        if isinstance(result, dict):
            return jsonify(**result)
        else:
            raise InvalidType(type(result))
    return _func


@app.errorhandler(InvalidType)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
