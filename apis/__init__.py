#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from utils.errors import InvalidType
app = Flask(__name__)


@app.errorhandler(InvalidType)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
