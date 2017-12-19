#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from utils import errors


class EmailProperty(ndb.StringProperty):
    def _validate(self, value):
        if not isinstance(value, basestring):
            e = errors.InvalidType('expected an hoiuasghdoh')
            import logging
            logging.debug(e)
            raise e
