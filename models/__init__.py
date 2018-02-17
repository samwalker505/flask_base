#! /usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class PaginateModel(object):

    def __init__(self, results, next_cursor, prev_cursor, more):
        self.results = results
        self.next_cursor = next_cursor
        self.prev_cursor = prev_cursor
        self.more = more

    def to_dict(self, *args, **kwargs):
        p = {}
        num_of_items = len(self.results)
        p['num_of_items'] = num_of_items
        p['next_cursor'] = self.next_cursor.urlsafe() if self.next_cursor else None
        p['prev_cursor'] = self.prev_cursor.urlsafe() if self.prev_cursor else None
        p['more'] = self.more

        data = [r.to_dict() for r in self.results]

        return {'pagination': p, 'data': data}


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
        d['id'] = str(self.key.id())
        d['urlsafe'] = self.key.urlsafe()
        return d

    @classmethod
    def paginate(cls, *args, **kwargs):
        query = cls.build_query(*args, **kwargs)
        op = {}
        if 'cursor' in kwargs:
            op['start_cursor'] = ndb.Cursor(urlsafe=kwargs['cursor'])
        query_option = ndb.QueryOptions(**op)
        page_size = kwargs['per_page'] if 'per_page' in kwargs else 10
        results, cursor, more = query.fetch_page(page_size, options=query_option)
        return PaginateModel(results, cursor, query_option.start_cursor, more)

    @classmethod
    def public_filters(cls, *args, **kwargs):
        return [] + cls.normal_filters()

    @classmethod
    def normal_filters(cls, *args, **kwargs):
        return [] + cls.admin_filters()

    @classmethod
    def admin_filters(cls, *args, **kwargs):
        return []
