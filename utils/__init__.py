from functools import wraps
from .errors import InvalidType
from flask import jsonify


def json_output(func):
    @wraps(func)
    def _func(*args, **kwds):
        result = func(*args, **kwds)
        if isinstance(result, dict):
            return jsonify(**result)
        else:
            raise InvalidType(type(result))
    return _func
