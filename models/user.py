#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from models import BaseModel
from utils import properties, errors

import json


class FacebookSSOMixin(object):

    @classmethod
    def from_fat(cls, fat):
        from externals.facebook import FacebookApi
        api = FacebookApi(access_token=fat)
        result = api.me(fields=['email', 'id', 'name'])
        if result.status_code == 200:
            fb_result = json.loads(result.content)
            fb_result['fb_id'] = fb_result['id']
            user = cls.create_or_connect(**fb_result)
            return user

    @classmethod
    def create_or_connect(cls, email=None, fb_id=None, name=None, **kwargs):
        email_log = Email.get_or_insert(email)
        if email_log.user_key:
            user = email_log.user_key.get()
            if not user:
                raise errors.ApiError('User is missing')
        else:
            user = User()

        user.email = email
        user.name = name
        user.fb_id = fb_id

        user_key = user.put()
        if not email_log.user_key:
            email_log.user_key = user_key
            email_log.put()

        return user


class User(FacebookSSOMixin, BaseModel):
    email = properties.EmailProperty()
    name = ndb.StringProperty()
    fb_id = ndb.StringProperty()


class Email(ndb.Model):
    user_key = ndb.KeyProperty()
