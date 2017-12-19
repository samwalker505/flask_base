#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import vendor
import tempfile

# monkey patch for temp file
tempfile.SpooledTemporaryFile = tempfile.TemporaryFile
# Add any libraries installed in the "lib" folder.
vendor.add('env')
