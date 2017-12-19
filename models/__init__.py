#! /usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    ctime = ndb.DateTimeProperty(auto_now_add=True)
    mtime = ndb.DateTimeProperty(auto_now=True)
