#! /usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import calendar
from datetime import datetime

from google.appengine.ext import ndb
from flask import jsonify, Flask, Response
from flask.json import JSONEncoder

from utils.errors import ApiError, InvalidType


class JSONResponse(Response):

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        else:
            raise InvalidType(type(rv))
        return super(JSONResponse, cls).force_type(rv, environ)


class JSONFlask(Flask):

    response_class = JSONResponse


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)



def admin_only(func):
    @wraps(func)
    def _func(*args, **kwds):
        from flask_jwt_extended import get_jwt_claims
        from models.user import UserRolesProperty
        import logging
        claims = get_jwt_claims()
        logging.debug('jwt claims: {}'.format(claims))
        if UserRolesProperty.ADMIN in claims['roles']:
            return func(*args, **kwds)
        else:
            raise ApiError('User is not Admin')
    return _func
