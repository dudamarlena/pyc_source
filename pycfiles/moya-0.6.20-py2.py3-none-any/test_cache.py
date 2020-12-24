# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_cache.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
import unittest, time
from fs.memoryfs import MemoryFS
from moya import cache
from nose.plugins.attrib import attr
try:
    import pylibmc
except:
    pylibmc = None

@attr(b'slow')
class CacheTests(object):
    long_key = b'longkey' * 100

    def setUp(self):
        print self

    def tearDown(self):
        pass

    def test_long_key(self):
        """Test long keys"""
        key = self.long_key
        value = [b'hello', b'world']
        self.assertEqual(self.cache.get(key, None), None)
        self.cache.set(key, value)
        self.assertEqual(self.cache.get(key, None), value)
        self.assertEqual(self.cache.get(b'nokey', None), None)
        return

    def test_set(self):
        """Test set/get"""
        value = [
         b'hello', b'world']
        self.assertEqual(self.cache.get(b'key', None), None)
        self.cache.set(b'key', value)
        self.assertEqual(self.cache.get(b'key', None), value)
        self.assertEqual(self.cache.get(b'nokey', None), None)
        self.cache.set(b'key2', b'ZZZZ')
        self.assertEqual(self.cache.get(b'key2'), b'ZZZZ')
        self.cache.set(b'key2', b'XXXX')
        self.assertEqual(self.cache.get(b'key2'), b'XXXX')
        return

    def test_set_time(self):
        """Test set with expire time"""
        value = [
         b'hello', b'world']
        self.cache.set(b'key', value, time=1000)
        self.assertEqual(self.cache.get(b'key', None), value)
        time.sleep(1.1)
        self.assertEqual(self.cache.get(b'key', None), None)
        return

    def test_delete(self):
        """Test delete"""
        value = [
         b'hello', b'world']
        self.assertEqual(self.cache.get(b'key', None), None)
        self.cache.set(b'key', value)
        self.assertEqual(self.cache.get(b'key', None), value)
        self.cache.delete(b'key')
        self.assertEqual(self.cache.get(b'key', None), None)
        return

    def test_contains(self):
        """Test contains"""
        value = [
         b'hello', b'world']
        self.assert_(not self.cache.contains(b'key'))
        self.assert_(b'key' not in self.cache)
        self.cache.set(b'key', value)
        self.assert_(self.cache.contains(b'key'))
        self.assert_(b'key' in self.cache)
        self.cache.delete(b'key')
        self.assert_(not self.cache.contains(b'key'))
        self.assert_(b'key' not in self.cache)


class NamespacesTests(object):
    """For caches that share storage"""

    def test_namespaces(self):
        """Test multiple namespaces on cache"""
        value = [
         b'hello', b'world']
        value2 = [b'goodybye', b'world']
        self.cache.set(b'key', value)
        self.assert_(b'key' in self.cache)
        self.assert_(b'key' not in self.cache2)
        self.cache2.set(b'key', value2)
        self.assertEqual(self.cache.get(b'key', None), value)
        self.assertEqual(self.cache2.get(b'key', None), value2)
        return


class TestDictCache(unittest.TestCase, CacheTests):

    def setUp(self):
        self.cache = cache.dictcache.DictCache(b'test', b'')


class TestMemoryCache(unittest.TestCase, CacheTests):

    def setUp(self):
        self.cache = cache.memorycache.MemoryCache(b'test', b'')


class TestFileCache(unittest.TestCase, CacheTests, NamespacesTests):
    __test__ = True

    def setUp(self):
        self.fs = MemoryFS()
        self.cache = cache.filecache.FileCache(b'test', b'ns1', fs=self.fs)
        self.cache2 = cache.filecache.FileCache(b'test', b'ns2', fs=self.fs)

    def tearDown(self):
        self.fs.close()
        self.fs = None
        return


class TestMemcacheCache(unittest.TestCase, CacheTests, NamespacesTests):
    __test__ = bool(pylibmc)

    def setUp(self):
        self.cache = cache.memcache.MemCache(b'test', b'ns1', hosts=[b'127.0.0.1'])
        self.cache2 = cache.memcache.MemCache(b'test', b'ns2', hosts=[b'127.0.0.1'])

    def tearDown(self):
        self.cache.delete(b'key')
        self.cache2.delete(b'key')
        self.cache.delete(CacheTests.long_key)
        self.cache2.delete(CacheTests.long_key)


class TestDictCompressCache(unittest.TestCase, CacheTests):
    """Test with compression enabled"""
    __test__ = True

    def setUp(self):
        self.cache = cache.dictcache.DictCache(b'test', b'', compress=True, compress_min=1)


class TestDebugWrapper(unittest.TestCase, CacheTests):
    __test__ = True

    def setUp(self):
        self._cache = cache.dictcache.DictCache(b'test', b'')
        self.cache = cache.base.DebugCacheWrapper(self._cache)


class TetstDisabledCache(unittest.TestCase):
    __test__ = True

    def setUp(self):
        self.cache = cache.disabledcache.DisabledCache(b'test', b'')

    def test_disabled(self):
        """Test disabled cache"""
        value = [
         b'hello', b'world']
        self.assert_(not self.cache.contains(b'key'))
        self.cache.set(b'key', value)
        self.assert_(not self.cache.contains(b'key'))
        self.assertEqual(self.cache.get(b'key', None), None)
        self.cache.delete(b'key')
        return