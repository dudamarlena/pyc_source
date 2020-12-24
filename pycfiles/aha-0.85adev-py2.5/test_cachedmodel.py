# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/model/tests/test_cachedmodel.py
# Compiled at: 2010-10-20 22:45:31
import os, unittest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import datastore_file_stub
from google.appengine.api import mail_stub
from google.appengine.api import urlfetch_stub
from google.appengine.api import user_service_stub
from google.appengine.ext import db, search
from nose.tools import *
from google.appengine.api import users
from google.appengine.api import memcache
from coregae.model.cachedmodel import *
from application.model.basictype import *
APP_ID = os.environ['APPLICATION_ID']
AUTH_DOMAIN = 'gmail.com'
LOGGED_IN_USER = 'test@example.com'

class GAETestBase(unittest.TestCase):

    def setUp(self):
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('memcache', memcache_stub.MemcacheServiceStub())
        stub = datastore_file_stub.DatastoreFileStub(APP_ID, '/dev/null', '/dev/null')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)


from coregae.model.cachedmodel import *

class CacheTest(GAETestBase):

    def test_cached_models(self):

        class CM(CachedModelBase):
            int_id = db.IntegerProperty(required=True)
            name = db.StringProperty(required=True)

        class CMT(CachedModelBase):
            int_id2 = db.IntegerProperty(required=True)
            name2 = db.StringProperty(required=True)

        a = CM(int_id=1, name='hoge')
        assert_false(a.cached)
        a.put()
        b = CM._get(a.key())
        assert_true(isinstance(b, dict))
        assert_true(sorted(b.keys()), sorted(['int_id', 'name']))
        d = CM.get(a.key())
        assert_true(isinstance(d, CM))
        assert_true(d.cached)
        assert_true(str(d.key()), str(a.key()))
        e = CM.get(a.key())
        assert_true(isinstance(e, CM))
        assert_true(e.cached)
        f = CM.get(a.key(), force=True)
        assert_true(isinstance(f, CM))
        assert_false(f.cached)
        memcache.flush_all()
        h = CM.get(a.key())
        assert_true(isinstance(h, CM))
        assert_false(h.cached)
        h = CM.get(a.key())
        assert_true(h.cached)
        assert_true('int_id' in h._dic)
        assert_equal(h.int_id, 1)
        h.int_id = 2
        assert_equal(h.int_id, 2)
        i = CM.get(a.key(), force=True)
        assert_equal(i.int_id, 1)
        h.put()
        i = CM.get(a.key(), force=True)
        assert_equal(i.int_id, 2)
        j = CMT(int_id2=0, name2='foo')
        assert_not_equal(CM.__SAVED_PROPS__, CMT.__SAVED_PROPS__)
        assert_not_equal(i.__SAVED_PROPS__, j.__SAVED_PROPS__)
        CMT.__SAVED_PROPS__ = []
        j = CMT(int_id2=0, name2='foo')
        assert_equal(sorted(CMT.__SAVED_PROPS__), sorted(['int_id2', 'name2']))
        CMT.__SAVED_PROPS__ = ['int_id2', 'name2', 'foo']
        j = CMT(d={'1': 1})
        assert_equal(sorted(CMT.__SAVED_PROPS__), sorted(['int_id2', 'name2', 'foo']))

    def test_partialcached_models(self):

        class CM2(CachedModelBase):
            CACHE_PROPS = ('int_id', )
            int_id = db.IntegerProperty(required=True)
            name = db.StringProperty(required=True)

        a = CM2(int_id=1, name='hoge')
        a.int_id = 2
        a.put()
        b = CM2.get(a.key())
        assert_equal(b.int_id, 2)
        a.name = 'foo'
        assert_equal(a.name, 'foo')
        a.put()
        b = CM2.get(a.key(), force=True)
        assert_equal(b.name, 'foo')
        b = CM2.get(a.key())
        assert_equal(b.name, None)
        a = CM2(int_id=1, name='hoge', cache=False)
        a.put(cache=False)
        b = CM2.get(a.key())
        assert_false(b.cached)
        return

    def test_cached_query(self):

        class CM3(CachedModelBase):
            ADD_PROPS = ('foo', 'bar')
            int_id = db.IntegerProperty(required=True)
            name = db.StringProperty(required=True)

        ol = []
        for i in range(20):
            o = CM3(int_id=i, name='name%d' % i)
            o.put()
            ol.append(o)

        for i in ol:
            CM3.get(i.key())

        q = CM3.all()
        assert_true(hasattr(q, 'cls'))
        assert_true(hasattr(q, 'query'))
        q.filter('int_id >', 10)
        nl = list(q.fetch(10))
        q = CM3.all()
        q.filter('int_id >', 10)
        nl = list(q.fetch(10))
        for i in nl:
            assert_true(i.cached)

        q = CM3.all()
        q.filter('int_id >', 20)
        q.order('-int_id')
        nl = list(q.fetch(10))
        q = CM3.all()
        q.filter('int_id >', 10)
        q.order('-int_id')
        nl = list(q.fetch(10, offset=5))
        q.filter('int_id >', 10)
        q.order('-int_id')
        nl = list(q.fetch(10, offset=5))
        for i in nl:
            assert_true(i.cached)

        q = CM3.all()
        q.order('-int_id')
        q.filter('int_id >', 10)
        q.flush_cache()
        nl = list(q.fetch(10))
        q = CM3.all()
        q.order('-int_id')
        q.filter('int_id >', 10)
        nl = list(q.fetch(10))
        nl = list(q.fetch(10, offset=5))
        q.flush_cache()
        q = CM3.all()
        q.order('-int_id')
        q.filter('int_id >', 10)
        nl = list(q.fetch(10, offset=5))
        q = CM3.all()
        q.order('-int_id')
        nl = list(q.fetch(10))
        nl[0].foo = 'foo'
        nl[0].cache()
        n = CM3.get(nl[0].key())
        assert_equal(n.foo, 'foo')
        q = CM3.all()
        q.order('-int_id')
        q.flush_cache()
        q = CM3.all()
        q.order('-int_id')
        nl = list(q.fetch(10))
        n = CM3.get(nl[0].key())
        assert_equal(n.foo, 'foo')
        q = CM3.all()
        assert_eaual(q.count(), q.count(force=True))
        q = CM3.all()
        q.filter('int_id >', 10)
        assert_eaual(q.count(), q.count(force=True))