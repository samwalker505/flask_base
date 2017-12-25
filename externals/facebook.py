#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseApi


class FacebookApi(BaseApi):

    def __init__(self, access_token):
        base_url = 'https://graph.facebook.com'
        super(FacebookApi, self).__init__(base_url)
        self.access_token = access_token

    def me(self, fields=None):
        q = {'access_token': self.access_token}
        if fields:
            f = ','.join(fields)
            p = {'fields': f}
            q.update(p)
        return self.get('/me', query=q)
