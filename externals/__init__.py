#! /usr/bin/env python
# -*- coding: utf-8 -*-


from google.appengine.api import urlfetch


class BaseApi(object):

    url = None
    headers = None

    def __init__(self, base, headers):
        self.url = base
        self.headers = headers

    def get(self, url, query=None, headers=None):
        import urllib
        q = urllib.urlencode(query)
        fetch_url = '{base}{url}?{q}'.format(base=self.url, url=url, q=query)
        h = self.get_headers(headers)
        if h:
            r = urlfetch.fetch(fetch_url, headers=h)
        else:
            r = urlfetch.fetch(fetch_url)
        return r

    def post(self, url, params, headers=None):
        fetch_url = '{base}{url}'.format(base=self.url, url=url)
        h = self.get_headers(headers) or {}
        h['Content-Type'] = 'application/json'
        import json
        r = urlfetch.fetch(fetch_url, headers=h, method=urlfetch.POST, payload=json.dumps(params))
        return r

    def get_headers(self, headers):
        if self.headers and headers:
            h = self.headers + headers
        elif headers:
            h = headers
        elif self.headers:
            h = self.headers
        else:
            h = None

        return h
