#! /usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import vendor
import tempfile
import utils.tempfile2

# monkey patch for temp file
tempfile.SpooledTemporaryFile = utils.tempfile2.SpooledTemporaryFile
# Add any libraries installed in the "lib" folder.
vendor.add('lib')
