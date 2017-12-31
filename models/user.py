#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from google.appengine.ext import ndb
from models import BaseModel
from utils import properties, errors


class UserRolesProperty(ndb.StringProperty):

    NORMAL = 'normal'
    ADMIN = 'admin'

    values = [NORMAL, ADMIN]

    def _validate(self, value):
        if value not in self.values:
            raise errors.InvalidType(self.__class__.__name__)


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
        else:
            error = json.loads(result.content)['error']
            raise errors.ApiError(error['message'], payload={'facebook_response': error})

    @classmethod
    def create_or_connect(cls, email=None, fb_id=None, name=None, **kwargs):
        email_log = Email.get_or_insert(email)
        if email_log.user_key:
            user = email_log.user_key.get()
            if not user:
                raise errors.ApiError('User is missing')
        else:
            user = User()

        user.email = user.email or email
        user.name = user.name or name
        user.fb_id = user.fb_id or fb_id
        user.roles = user.roles or [UserRolesProperty.NORMAL]

        user_key = user.put()
        if not email_log.user_key:
            email_log.user_key = user_key
            email_log.put()

        return user


class User(FacebookSSOMixin, BaseModel):
    email = properties.EmailProperty()
    name = ndb.StringProperty()
    fb_id = ndb.StringProperty()
    blocked = ndb.BooleanProperty(default=False)
    roles = UserRolesProperty(repeated=True)

    @property
    def is_admin(self):
        import logging
        logging.debug(self.roles)
        logging.debug(UserRolesProperty.ADMIN in self.roles)
        return UserRolesProperty.ADMIN in self.roles

    @classmethod
    def public_filters(cls):
        return ['blocked']

    @classmethod
    def build_query(cls, *args, **kwargs):
        return cls.query().order(-cls.ctime)


class Email(ndb.Model):
    user_key = ndb.KeyProperty()
