#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from werkzeug.utils import secure_filename
from google.appengine.ext import ndb, blobstore
from models import BaseModel
from utils import errors
import cloudstorage as gcs
from google.appengine.api import images
from google.appengine.api import app_identity


#### ADD EXTENSIONS ~! HO IMPORTANT
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'raw', 'gif', 'png'])


PUBLIC_NAMESPACE = 'PUBLIC'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _get_options(upload_file):
    extension = secure_filename(upload_file.filename).rsplit('.', 1)[1]
    options = {}
    options['retry_params'] = gcs.RetryParams(backoff_factor=1.1)
    options['content_type'] = 'image/' + extension
    return options


def _get_path(upload_file, user_key):
    namespace = user_key.urlsafe() if user_key else PUBLIC_NAMESPACE
    bucket_name = os.environ.get('BUCKET_NAME',
                           app_identity.get_default_gcs_bucket_name())
    path = '/' + bucket_name + '/' + namespace + '/' + str(secure_filename(upload_file.filename))
    return path


class ResourceType(object):
    IMAGE = 'image'
    ALL = [IMAGE, ]


class Resource(BaseModel):

    res_type = ndb.StringProperty(default=ResourceType.IMAGE)
    storage_url = ndb.StringProperty()
    user_key = ndb.KeyProperty()

    @classmethod
    def create(cls, upload_file, res_type=None, user_key=None):
        res = cls._create(upload_file, res_type, user_key)
        res.put()
        return res

    @classmethod
    def _create(cls, upload_file, res_type=None, user_key=None):
        if res_type is None:
            raise errors.ApiError('NO_RESOURCE_TYPE')
        if res_type not in ResourceType.ALL:
            raise errors.ApiError('INCORRECT_RESOURCE_TYPE')
        if not allowed_file(upload_file.filename):
            raise errors.InvalidType('INVALID_EXTENSION')
        options = _get_options(upload_file)
        path = _get_path(upload_file, user_key)
        try:
            with gcs.open(path, 'w', **options) as f:
                f.write(upload_file.stream.read())# instead of f.write(str(file))
                logging.debug('uploaded file')
                res = cls(res_type = res_type, storage_url=path, user_key=user_key)
                return res
        except Exception as e:
            raise errors.ApiError(e.message)


    @classmethod
    def public_filters(cls):
        return ['user_key']

    @classmethod
    def build_query(cls, *args, **kwargs):
        return cls.query().order(-cls.ctime)


class Image(Resource):

    info = ndb.Expando()
    serving_url = ndb.StringProperty()

    @classmethod
    def create(cls, upload_file, res_type=None, user_key=None):
        res = super(Image, cls)._create(upload_file, res_type, user_key)
        blobstore_filename = '/gs{}'.format(res.storage_url)
        blob_key = blobstore.create_gs_key(blobstore_filename)
        url = images.get_serving_url(blob_key)
        res.serving_url = url
        res.put()
        return res
