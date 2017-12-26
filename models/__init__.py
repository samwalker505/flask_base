#! /usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    ctime = ndb.DateTimeProperty(auto_now_add=True)
    mtime = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self, *args, **kwargs):
        from flask_jwt_extended import get_current_user
        current_user = get_current_user()
        kls = self.__class__
        if current_user and current_user.is_admin:
            d = super(BaseModel, self).to_dict(exclude=kls.admin_filters(*args, **kwargs))
        elif current_user:
            d = super(BaseModel, self).to_dict(exclude=kls.normal_filters(*args, **kwargs))
        else:
            d = super(BaseModel, self).to_dict(exclude=kls.public_filters(*args, **kwargs))
        return d

    @classmethod
    def public_filters(cls, *args, **kwargs):
        return [] + cls.normal_filters()

    @classmethod
    def normal_filters(cls, *args, **kwargs):
        return [] + cls.admin_filters()

    @classmethod
    def admin_filters(cls, *args, **kwargs):
        return []
