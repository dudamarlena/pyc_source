# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/cache/tests/test_backend.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import inspect, zlib
from django.core.cache import cache
from django.utils.six.moves import cPickle as pickle
from kgb import SpyAgency
from djblets.cache.backend import cache_memoize, cache_memoize_iter, make_cache_key, CACHE_CHUNK_SIZE
from djblets.testing.testcases import TestCase

class CacheTests(SpyAgency, TestCase):

    def tearDown(self):
        super(CacheTests, self).tearDown()
        cache.clear()

    def test_cache_memoize(self):
        """Testing cache_memoize"""
        cacheKey = b'abc123'
        testStr = b'Test 123'

        def cacheFunc(cacheCalled=[]):
            self.assertTrue(not cacheCalled)
            cacheCalled.append(True)
            return testStr

        result = cache_memoize(cacheKey, cacheFunc)
        self.assertEqual(result, testStr)
        result = cache_memoize(cacheKey, cacheFunc)
        self.assertEqual(result, testStr)

    def test_cache_memoize_large_files_uncompressed(self):
        """Testing cache_memoize with large files without compression"""
        cache_key = b'abc123'
        data, pickled_data = self._build_test_chunk_data(num_chunks=2)

        def cache_func():
            return data

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=False)
        self.assertEqual(result, data)
        self.assertTrue(cache_func.spy.called)
        cache_key_0 = make_cache_key(b'%s-0' % cache_key)
        cache_key_1 = make_cache_key(b'%s-1' % cache_key)
        self.assertTrue(make_cache_key(cache_key) in cache)
        self.assertTrue(cache_key_0 in cache)
        self.assertTrue(cache_key_1 in cache)
        self.assertFalse(make_cache_key(b'%s-2' % cache_key) in cache)
        stored_data = (b'').join(cache.get(cache_key_0) + cache.get(cache_key_1))
        self.assertEqual(stored_data, pickled_data)
        cache_func.spy.reset_calls()
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=False)
        self.assertEqual(result, data)
        self.assertFalse(cache_func.spy.called)

    def test_cache_memoize_large_files_uncompressed_off_by_one(self):
        """Testing cache_memoize with large files without compression and
        one byte larger than an even chunk size."""
        cache_key = b'abc123'
        data = self._build_test_chunk_data(num_chunks=2)[0] + b'x'
        pickled_data = pickle.dumps(data)

        def cache_func():
            return data

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=False)
        self.assertEqual(result, data)
        self.assertTrue(cache_func.spy.called)
        cache_key_0 = make_cache_key(b'%s-0' % cache_key)
        cache_key_1 = make_cache_key(b'%s-1' % cache_key)
        cache_key_2 = make_cache_key(b'%s-2' % cache_key)
        self.assertTrue(make_cache_key(cache_key) in cache)
        self.assertTrue(cache_key_0 in cache)
        self.assertTrue(cache_key_1 in cache)
        self.assertTrue(cache_key_2 in cache)
        self.assertFalse(make_cache_key(b'%s-3' % cache_key) in cache)
        stored_data = (b'').join(cache.get(cache_key_0) + cache.get(cache_key_1) + cache.get(cache_key_2))
        self.assertEqual(stored_data, pickled_data)
        cache_func.spy.reset_calls()
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=False)
        self.assertEqual(result, data)
        self.assertFalse(cache_func.spy.called)

    def test_cache_memoize_large_files_compressed(self):
        """Testing cache_memoize with large files with compression"""
        cache_key = b'abc123'
        data, pickled_data = self._build_test_chunk_data(num_chunks=2)

        def cache_func():
            return data

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=True)
        self.assertTrue(cache_func.spy.called)
        cache_key_0 = make_cache_key(b'%s-0' % cache_key)
        self.assertTrue(make_cache_key(cache_key) in cache)
        self.assertTrue(cache_key_0 in cache)
        self.assertFalse(make_cache_key(b'%s-1' % cache_key) in cache)
        self.assertFalse(make_cache_key(b'%s-2' % cache_key) in cache)
        stored_data = cache.get(cache_key_0)[0]
        self.assertEqual(stored_data, zlib.compress(pickled_data))
        cache_func.spy.reset_calls()
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=True)
        self.assertEqual(result, data)
        self.assertFalse(cache_func.spy.called)

    def test_cache_memoize_large_files_load_uncompressed(self):
        """Testing cache_memoize with large files without compression and
        loading data
        """
        cache_key = b'abc123'
        data, pickled_data = self._build_test_chunk_data(num_chunks=2)
        cache.set(make_cache_key(cache_key), b'2')
        cache.set(make_cache_key(b'%s-0' % cache_key), [
         pickled_data[:CACHE_CHUNK_SIZE]])
        cache.set(make_cache_key(b'%s-1' % cache_key), [
         pickled_data[CACHE_CHUNK_SIZE:]])

        def cache_func():
            return b''

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=False)
        self.assertEqual(result, data)
        self.assertFalse(cache_func.spy.called)

    def test_cache_memoize_large_files_load_compressed(self):
        """Testing cache_memoize with large files with compression and
        loading cached data
        """
        cache_key = b'abc123'
        data, pickled_data = self._build_test_chunk_data(num_chunks=2)
        stored_data = zlib.compress(pickled_data)
        self.assertTrue(len(stored_data) < CACHE_CHUNK_SIZE)
        cache.set(make_cache_key(cache_key), b'1')
        cache.set(make_cache_key(b'%s-0' % cache_key), [stored_data])

        def cache_func():
            return b''

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=True)
        self.assertEqual(result, data)
        self.assertFalse(cache_func.spy.called)

    def test_cache_memoize_large_files_missing_chunk(self):
        """Testing cache_memoize with loading large files with missing chunks
        """
        cache_key = b'abc123'
        data, pickled_data = self._build_test_chunk_data(num_chunks=2)
        cache.set(make_cache_key(cache_key), b'2')
        cache.set(make_cache_key(b'%s-0' % cache_key), [
         pickled_data[:CACHE_CHUNK_SIZE]])

        def cache_func():
            return data

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize(cache_key, cache_func, large_data=True, compress_large_data=False)
        self.assertEqual(len(result), len(data))
        self.assertEqual(result, data)
        self.assertTrue(cache_func.spy.called)

    def test_cache_memoize_iter_uncompressed(self):
        """Testing cache_memoize_iter without compression"""
        cache_key = b'abc123'
        data_yielded = []
        data1, pickled_data_1 = self._build_test_chunk_data(num_chunks=2)
        data2, pickled_data_2 = self._build_test_chunk_data(num_chunks=2)

        def cache_func():
            data_yielded.append(b'data1')
            yield data1
            data_yielded.append(b'data2')
            yield data2

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize_iter(cache_key, cache_func, compress_large_data=False)
        self.assertTrue(inspect.isgenerator(result))
        self.assertEqual(data_yielded, [])
        self.assertEqual(next(result), data1)
        self.assertEqual(data_yielded, [b'data1'])
        self.assertEqual(next(result), data2)
        self.assertEqual(data_yielded, [b'data1', b'data2'])
        with self.assertRaises(StopIteration):
            next(result)
        self.assertTrue(cache_func.spy.called)
        cache_key_main = make_cache_key(cache_key)
        cache_key_0 = make_cache_key(b'%s-0' % cache_key)
        cache_key_1 = make_cache_key(b'%s-1' % cache_key)
        cache_key_2 = make_cache_key(b'%s-2' % cache_key)
        cache_key_3 = make_cache_key(b'%s-3' % cache_key)
        self.assertTrue(cache_key_main in cache)
        self.assertTrue(cache_key_0 in cache)
        self.assertTrue(cache_key_1 in cache)
        self.assertTrue(cache_key_2 in cache)
        self.assertTrue(cache_key_3 in cache)
        self.assertFalse(make_cache_key(b'%s-4' % cache_key) in cache)
        stored_data = (b'').join(cache.get(cache_key_0) + cache.get(cache_key_1) + cache.get(cache_key_2) + cache.get(cache_key_3))
        self.assertEqual(cache.get(cache_key_main), b'4')
        self.assertEqual(stored_data, pickled_data_1 + pickled_data_2)
        cache_func.spy.reset_calls()
        data_yielded = []
        result = cache_memoize_iter(cache_key, cache_func, compress_large_data=False)
        self.assertTrue(inspect.isgenerator(result))
        self.assertEqual(next(result), data1)
        self.assertEqual(next(result), data2)
        with self.assertRaises(StopIteration):
            next(result)
        self.assertEqual(data_yielded, [])
        self.assertFalse(cache_func.spy.called)

    def test_cache_memoize_iter_compressed(self):
        """Testing cache_memoize_iter with compression"""
        cache_key = b'abc123'
        data_yielded = []
        data1, pickled_data_1 = self._build_test_chunk_data(num_chunks=2)
        data2, pickled_data_2 = self._build_test_chunk_data(num_chunks=2)

        def cache_func():
            data_yielded.append(b'data1')
            yield data1
            data_yielded.append(b'data2')
            yield data2

        self.spy_on(cache_func, call_original=True)
        result = cache_memoize_iter(cache_key, cache_func, compress_large_data=True)
        self.assertTrue(inspect.isgenerator(result))
        self.assertEqual(data_yielded, [])
        self.assertEqual(next(result), data1)
        self.assertEqual(data_yielded, [b'data1'])
        self.assertEqual(next(result), data2)
        self.assertEqual(data_yielded, [b'data1', b'data2'])
        with self.assertRaises(StopIteration):
            next(result)
        self.assertTrue(cache_func.spy.called)
        cache_key_main = make_cache_key(cache_key)
        cache_key_0 = make_cache_key(b'%s-0' % cache_key)
        self.assertTrue(cache_key_main in cache)
        self.assertTrue(cache_key_0 in cache)
        self.assertFalse(make_cache_key(b'%s-1' % cache_key) in cache)
        self.assertEqual(cache.get(cache_key_main), b'1')
        self.assertEqual(cache.get(cache_key_0)[0], zlib.compress(pickled_data_1 + pickled_data_2))
        cache_func.spy.reset_calls()
        data_yielded = []
        result = cache_memoize_iter(cache_key, cache_func, compress_large_data=True)
        self.assertTrue(inspect.isgenerator(result))
        self.assertEqual(next(result), data1)
        self.assertEqual(next(result), data2)
        with self.assertRaises(StopIteration):
            next(result)
        self.assertEqual(data_yielded, [])
        self.assertFalse(cache_func.spy.called)

    def _build_test_chunk_data(self, num_chunks):
        """Build enough test data to fill up the specified number of chunks.

        This takes into account the size of the pickle data, and will
        get us to exactly the specified number of chunks of data in the cache.
        """
        data = b'x' * (CACHE_CHUNK_SIZE * num_chunks - 3 * num_chunks)
        pickled_data = pickle.dumps(data)
        self.assertEqual(len(pickled_data), CACHE_CHUNK_SIZE * num_chunks)
        return (
         data, pickled_data)