# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/tests/test_cache.py
# Compiled at: 2012-01-22 12:14:35
import unittest, sqlalchemy
from lazy_slides.cache import open_cache
from lazy_slides.tests.util import remove, temp_file

class CacheTest(unittest.TestCase):

    def setUp(self):
        self.db_file = ':memory:'

    def test_get(self):
        engine = 'engine'
        tag = 'tag'
        filename = 'test_file'
        with open_cache(self.db_file, 1000) as (cache):
            self.assertEqual(cache.get(engine, tag), None)
            with temp_file(filename):
                cache.set(engine, tag, filename)
                self.assertEqual(cache.get(engine, tag), filename)
        return

    def test_get_missing_file(self):
        engine = 'engine'
        tag = 'tag'
        filename = 'test_file'
        with open_cache(self.db_file, 100) as (cache):
            with temp_file(filename):
                cache.set(engine, tag, filename)
                self.assertEqual(cache.get(engine, tag), filename)
            self.assertEqual(cache.get(engine, tag), None)
        return

    def test_set_overwrite(self):
        engine = 'engine'
        tag = 'tag'
        filename = 'temp_file'
        filename2 = 'temp_file2'
        with open_cache(self.db_file, 1000) as (cache):
            with temp_file(filename):
                cache.set(engine, tag, filename)
                self.assertEqual(cache.get(engine, tag), filename)
            with temp_file(filename2):
                cache.set(engine, tag, filename2)
                self.assertEqual(cache.get(engine, tag), filename2)

    def test_size(self):
        with open_cache(self.db_file, 1000) as (cache):
            self.assertEqual(cache.size(), 0)
            for i in range(100):
                cache.set('engine', str(i), str(i))
                self.assertEqual(cache.size(), i + 1)

    def test_trim(self):
        SIZE = 100
        with open_cache(self.db_file, 1000) as (cache):
            for i in range(SIZE):
                cache.set('engine', str(i), str(i))

            self.assertEqual(cache.size(), SIZE)
            NEW_SIZE = 40
            cache.trim(NEW_SIZE)
            self.assertEqual(cache.size(), NEW_SIZE)
            cache.trim(cache.size() + 1)
            self.assertEqual(cache.size(), NEW_SIZE)