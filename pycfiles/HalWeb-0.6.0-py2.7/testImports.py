# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/tests/testImports.py
# Compiled at: 2012-01-02 17:03:25
import imports, unittest, os
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util
from StringIO import StringIO
from google.appengine.ext import webapp
from lib.halicea.helpers import LazyDict, DynamicParameters
os.environ['HTTP_HOST'] = 'localhost'