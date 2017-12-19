#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import app
from utils.errors import InvalidType
from models.user import User


@app.route('/')
def get_foo():
    User(email=5678)
    raise InvalidType('This view is gone', status_code=410)
