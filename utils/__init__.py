#! /usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from .errors import ApiError, InvalidType
from flask import jsonify
from flask_jwt_extended import get_current_user


def json_output(func):
    @wraps(func)
    def _func(*args, **kwds):
        result = func(*args, **kwds)
        if isinstance(result, dict):
            return jsonify(**result)
        else:
            raise InvalidType(type(result))
    return _func


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


def output_exclude(public_exclude=None, normal_exclude=None, admin_exclude=None):
    def wrapper(func):
        @wraps(func)
        def _func(*args, **kwargs):
            user = get_current_user()
            import logging
            if user and user.is_admin:
                logging.debug('user is admin')
                fields = admin_exclude or []
            elif user:
                logging.debug('user is normal')
                fields = normal_exclude or []
            else:
                logging.debug('is public')
                fields = public_exclude or []
            r = func(*args, **kwargs)
            if isinstance(r, dict):
                for f_name in fields:
                    if f_name in r:
                        del r[f_name]
                return r
            elif isinstance(r, list):
                new_list = []
                for el in r:
                    for f_name in fields:
                        if f_name in el:
                            del el[f_name]
                    new_list.append(el)
                return new_list

        return _func
    return wrapper
