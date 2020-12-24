# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bilbo/Projects/playground/redis_cache/tests/test_default_cache.py
# Compiled at: 2012-12-22 13:12:45
from redis import Redis
import time
from unittest import TestCase
from redcache import default_cache
from redcache.connection import get_current_connection, pop_connection, push_connection

class DefaultCacheManagerTestCase(TestCase):

    def setUp(self):
        push_connection(Redis())

    def tearDown(self):
        pop_connection()

    def test_default_ttl(self):

        @default_cache.cache
        def default_test1(a):
            return {'a': a}

        default_test1('spam')
        redis = get_current_connection()
        assert redis.ttl('cache:default_test1:spam') is None
        redis.delete('cache:default_test1:spam')
        return

    def test_custom_ttl(self):

        @default_cache.cache(ttl=5)
        def default_test2(a):
            return {'a': a}

        default_test2('eggs')
        time.sleep(6)
        redis = get_current_connection()
        assert redis.get('cache:default_test2:spam') is None
        return