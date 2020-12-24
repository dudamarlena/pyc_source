# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/model/tests/test_lazyloadingmodel.py
# Compiled at: 2010-10-20 22:45:29
import os, unittest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import mail_stub
from google.appengine.api import urlfetch_stub
from google.appengine.api import user_service_stub
from google.appengine.ext import db, search
from nose.tools import *
from google.appengine.api import users
APP_ID = os.environ['APPLICATION_ID']
AUTH_DOMAIN = 'gmail.com'
LOGGED_IN_USER = 'test@example.com'

class GAETestBase(unittest.TestCase):

    def setUp(self):
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        stub = datastore_file_stub.DatastoreFileStub(APP_ID, '/dev/null', '/dev/null')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)


from application.model.lab import *

class LazyTest(GAETestBase):

    def test_lazy_string_property(self):

        class TestModel(LazyModelBase):
            st1 = db.StringProperty(required=False, default='')
            ls1 = LazyStringProperty()
            lazykey_ls1 = db.StringProperty(required=False, default='')

        tm = TestModel()
        tm.ls1 = 'foo'
        assert_equal(tm.ls1, 'foo')
        tm.put()
        k = tm.key()
        tm2 = TestModel.get(k)
        assert_equal(tm2.ls1, 'foo')

    def test_lazy_metaclass(self):

        class TestMetaModel(LazyModelBase):
            __metaclass__ = LazyLoadingMetaclass
            st1 = db.StringProperty(required=False, default='')
            ls1 = LazyStringProperty()

        tm = TestMetaModel()
        assert_equal(tm.lazy_properties, ['st1'])
        tm.ls1 = 'foo'
        assert_equal(tm.ls1, 'foo')
        tm.put()
        k = tm.key()
        tm2 = TestMetaModel.get(k)
        assert_equal(tm2.ls1, 'foo')