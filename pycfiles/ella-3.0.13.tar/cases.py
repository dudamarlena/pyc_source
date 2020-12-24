# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/cases.py
# Compiled at: 2013-11-22 05:24:18
from django.test import TestCase
from ella.core.cache.redis import client

class RedisTestCase(TestCase):

    def tearDown(self):
        super(RedisTestCase, self).tearDown()
        client.flushdb()