# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bilbo/Projects/playground/redis_cache/tests/test_connection.py
# Compiled at: 2012-12-22 13:12:45
import redis
from unittest import TestCase
import redcache.connection

class ConnectionTestCase(TestCase):

    def test_connect(self):
        redcache.connection.use_connection()
        connection = redcache.connection.get_current_connection()
        assert connection.echo('I work') == 'I work'

    def test_use_connection(self):
        r = redis.Redis()
        redcache.connection.use_connection(r)
        connection = redcache.connection.get_current_connection()
        assert connection == r
        assert connection.echo('I work') == 'I work'