#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from models import BaseModel
from utils import properties


class User(BaseModel):
    email = properties.EmailProperty()
