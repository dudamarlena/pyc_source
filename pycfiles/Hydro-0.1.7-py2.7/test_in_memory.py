# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/test/hydro/cache/test_in_memory.py
# Compiled at: 2016-03-22 15:09:41
import unittest
from django.conf import settings
__author__ = 'moshebasanchig'

class InMemoryCacheTest(unittest.TestCase):

    def setUp(self):
        if not settings.configured:
            settings.configure()
        from hydro.cache.in_memory import InMemoryCache
        self.cache = InMemoryCache()
        self.cache.put('1', [1, 2, 3])

    def test_cache_miss(self):
        data = self.cache.get('2')
        self.assertIsNone(data)

    def test_cache_hit(self):
        data = self.cache.get('1')
        self.assertListEqual(data, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()