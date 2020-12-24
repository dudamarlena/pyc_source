# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev_ws\wrapcache\wrapcache\adapter\MemoryAdapter.py
# Compiled at: 2016-01-11 20:27:09
"""
Memory Adapter object.
"""
import time
from wrapcache.adapter.BaseAdapter import BaseAdapter
from wrapcache.adapter.CacheException import CacheExpiredException

class MemoryAdapter(BaseAdapter):
    """
        use for memory cache
        """

    def __init__(self, timeout=-1):
        super(MemoryAdapter, self).__init__(timeout=timeout)
        if MemoryAdapter.db is None:
            MemoryAdapter.db = {}
        return

    def get(self, key):
        cache = MemoryAdapter.db.get(key, {})
        if time.time() - cache.get('time', 0) > 0:
            self.remove(key)
            raise CacheExpiredException(key)
        else:
            return cache.get('value', None)
        return

    def set(self, key, value):
        cache = {'value': value, 'time': time.time() + self.timeout}
        MemoryAdapter.db[key] = cache
        return True

    def remove(self, key):
        return MemoryAdapter.db.pop(key, {}).get('value', None)

    def flush(self):
        MemoryAdapter.db.clear()
        return True


if __name__ == '__main__':
    import unittest

    class TestCase(unittest.TestCase):

        def setUp(self):
            self.test_class = MemoryAdapter(timeout=3)

        def tearDown(self):
            pass

        def test_init_db_with_singleton(self):
            pre_db = self.test_class.db
            new_adapter = MemoryAdapter(timeout=1)
            cur_db = new_adapter.db
            self.assertEqual(id(pre_db), id(cur_db))

        def test_memory_adapter(self):
            key = 'test_key_1'
            value = str(time.time())
            self.test_class.set(key, value)
            self.assertEqual(self.test_class.get(key), value)
            time.sleep(4)
            self.assertRaises(CacheExpiredException, self.test_class.get, key)
            self.test_class.set(key, value)
            self.test_class.remove(key)
            self.assertRaises(CacheExpiredException, self.test_class.get, key)
            self.test_class.set(key, value)
            self.test_class.flush()
            self.assertRaises(CacheExpiredException, self.test_class.get, key)


    unittest.main()