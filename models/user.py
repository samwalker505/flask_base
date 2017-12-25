#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from models import BaseModel
from utils import properties


class FacebookSSO(ndb.Model):
    fbid = ndb.StringProperty(required=True)
    user = ndb.KeyProperty(required=True)


class FacebookSSOMixin(object):

    def create_from_fat(fat):
        from externals.facebook import FacebookApi
        api = FacebookApi(access_token=fat)
        return api.me()


class User(BaseModel):
    email = properties.EmailProperty()
    name = ndb.StringProperty()


class Email(ndb.Model):
    user = ndb.KeyProperty(required=True)
