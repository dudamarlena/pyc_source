# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/switchcache/test.py
# Compiled at: 2014-05-09 16:02:50
from nose.tools import raises
from switchcache import *
from switchcache import NotConfiguredYet
import memcache

class Configure:
    HOSTS = [
     '127.0.0.1:11211']
    CACHE = {'foo': 'bar', 
       'fuga': 'hoge'}


mc = memcache.Client(Configure.HOSTS)

class TestNotConfigured:

    @raises(NotConfiguredYet)
    def test_no_cache_with_not_configured(self):
        no_cache(None)
        return

    @raises(NotConfiguredYet)
    def test_with_cache_with_not_configured(self):
        with_cache(None)
        return

    @raises(NotConfiguredYet)
    def test_with_clause_not_configuerd(self):
        with cache:
            pass


class TestConfigured:

    def setup(self):
        init(Configure)

        @with_cache
        def test_with_cache(s):
            for k, v in Configure.CACHE.items():
                assert mc.get(k) == v

            return s

        @no_cache
        def test_no_cache(s):
            for k, v in Configure.CACHE.items():
                assert mc.get(k) == None

            return s

        self.test_with_cache = test_with_cache
        self.test_no_cache = test_no_cache

    def test_with_cache_entity(self):
        assert self.test_with_cache('test') == 'test'

    def test_no_cache_entity(self):
        assert self.test_no_cache('test') == 'test'

    def test_with_clause(self):
        with cache:
            for k, v in Configure.CACHE.items():
                assert mc.get(k) == v

        for k, v in Configure.CACHE.items():
            assert mc.get(k) == None

        return

    def teardown(self):
        init(None)
        return


class TestTimes:

    def test_times(self):

        @times(3)
        def echo(x):
            return x

        ret = echo('test')
        assert ret == ['test', 'test', 'test']

    def test_twice(self):

        @twice
        def echo(x):
            return x

        ret = echo('test')
        assert ret == ['test', 'test']