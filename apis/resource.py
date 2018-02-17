#! /usr/bin/env python
# -*- coding: utf-8 -*-

from webargs import fields
from webargs.flaskparser import use_args
from flask import Blueprint, request
from flask_jwt_extended import (jwt_required,
                                jwt_optional,
                                get_current_user)
from utils import errors
from . import app
from models.resource import Image, Resource, ResourceType

# this one is intended to be the boilerplate for api

resource = Blueprint('Resource', __name__,)


@resource.route('/<res_type>', methods=['POST'])
@jwt_optional
def create_resource(res_type):
    if 'file' in request.files:
        _file = request.files['file']
        options = {
            'upload_file': _file,
            'res_type': res_type,
            'user_key': get_current_user()
        }
        if res_type == ResourceType.IMAGE:
            res = Image.create(**options)
        else:
            res = Resource.create(**options)
        return res.to_dict()
    else:
        raise errors.ApiError('NO_FILE_UPLOADED')


app.register_blueprint(resource, url_prefix='/resources')
