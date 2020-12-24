# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_2i.py
# Compiled at: 2016-10-17 19:06:50
import unittest
from riak import RiakError
from riak.tests import RUN_INDEXES
from riak.tests.base import IntegrationTestBase

class TwoITests(IntegrationTestBase, unittest.TestCase):

    def is_2i_supported(self):
        try:
            self.client.get_index('foo', 'bar_bin', 'baz')
            return True
        except Exception as e:
            if 'indexes_not_supported' in str(e):
                return False
            return True

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_secondary_index_store(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket = self.client.bucket(self.bucket_name)
        rand = self.randint()
        obj = bucket.new('mykey1', rand)
        obj.add_index('field1_bin', 'val1a')
        obj.add_index('field1_int', 1011)
        obj.store()
        obj = bucket.get('mykey1')
        self.assertEqual(['val1a'], [ y for x, y in obj.indexes if x == 'field1_bin'
                                    ])
        self.assertEqual([1011], [ y for x, y in obj.indexes if x == 'field1_int'
                                 ])
        obj.add_index('field1_bin', 'val1b')
        obj.add_index('field1_int', 1012)
        obj.store()
        obj = bucket.get('mykey1')
        self.assertEqual(['val1a', 'val1b'], sorted([ y for x, y in obj.indexes if x == 'field1_bin'
                                                    ]))
        self.assertEqual([1011, 1012], sorted([ y for x, y in obj.indexes if x == 'field1_int'
                                              ]))
        self.assertEqual([
         ('field1_bin', 'val1a'),
         ('field1_bin', 'val1b'),
         ('field1_int', 1011),
         ('field1_int', 1012)], sorted(obj.indexes))
        obj.remove_index('field1_bin', 'val1a')
        obj.remove_index('field1_int', 1011)
        obj.store()
        obj = bucket.get('mykey1')
        self.assertEqual(['val1b'], sorted([ y for x, y in obj.indexes if x == 'field1_bin'
                                           ]))
        self.assertEqual([1012], sorted([ y for x, y in obj.indexes if x == 'field1_int'
                                        ]))
        obj.add_index('field1_bin', 'val1a')
        obj.add_index('field1_bin', 'val1a')
        obj.add_index('field1_bin', 'val1a')
        obj.add_index('field1_int', 1011)
        obj.add_index('field1_int', 1011)
        obj.add_index('field1_int', 1011)
        self.assertEqual([
         ('field1_bin', 'val1a'),
         ('field1_bin', 'val1b'),
         ('field1_int', 1011),
         ('field1_int', 1012)], sorted(obj.indexes))
        obj.store()
        obj = bucket.get('mykey1')
        self.assertEqual([
         ('field1_bin', 'val1a'),
         ('field1_bin', 'val1b'),
         ('field1_int', 1011),
         ('field1_int', 1012)], sorted(obj.indexes))
        bucket.get('mykey1').delete()

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_set_indexes(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket = self.client.bucket(self.bucket_name)
        foo = bucket.new('foo', 1)
        foo.indexes = set([('field1_bin', 'test'), ('field2_int', 1337)])
        foo.store()
        result = self.client.index(self.bucket_name, 'field2_int', 1337).run()
        self.assertEqual(1, len(result))
        self.assertEqual('foo', result[0][1])
        result = bucket.get_index('field1_bin', 'test')
        self.assertEqual(1, len(result))
        self.assertEqual('foo', str(result[0]))

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_remove_indexes(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket = self.client.bucket(self.bucket_name)
        bar = bucket.new('bar', 1).add_index('bar_int', 1).add_index('bar_int', 2).add_index('baz_bin', 'baz').store()
        result = bucket.get_index('bar_int', 1)
        self.assertEqual(1, len(result))
        self.assertEqual(3, len(bar.indexes))
        self.assertEqual(2, len([ x for x in bar.indexes if x[0] == 'bar_int'
                                ]))
        bar = bar.remove_indexes().store()
        result = bucket.get_index('bar_int', 1)
        self.assertEqual(0, len(result))
        result = bucket.get_index('baz_bin', 'baz')
        self.assertEqual(0, len(result))
        self.assertEqual(0, len(bar.indexes))
        self.assertEqual(0, len([ x for x in bar.indexes if x[0] == 'bar_int'
                                ]))
        self.assertEqual(0, len([ x for x in bar.indexes if x[0] == 'baz_bin'
                                ]))
        bar = bar.add_index('bar_int', 1).add_index('bar_int', 2).add_index('baz_bin', 'baz').store()
        bar = bar.remove_index(field='bar_int').store()
        result = bucket.get_index('bar_int', 1)
        self.assertEqual(0, len(result))
        result = bucket.get_index('bar_int', 2)
        self.assertEqual(0, len(result))
        result = bucket.get_index('baz_bin', 'baz')
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(bar.indexes))
        self.assertEqual(0, len([ x for x in bar.indexes if x[0] == 'bar_int'
                                ]))
        self.assertEqual(1, len([ x for x in bar.indexes if x[0] == 'baz_bin'
                                ]))
        bar = bar.add_index('bar_int', 1).add_index('bar_int', 2).add_index('baz_bin', 'baz').store()
        bar = bar.remove_index(field='bar_int', value=2).store()
        result = bucket.get_index('bar_int', 1)
        self.assertEqual(1, len(result))
        result = bucket.get_index('bar_int', 2)
        self.assertEqual(0, len(result))
        result = bucket.get_index('baz_bin', 'baz')
        self.assertEqual(1, len(result))
        self.assertEqual(2, len(bar.indexes))
        self.assertEqual(1, len([ x for x in bar.indexes if x[0] == 'bar_int'
                                ]))
        self.assertEqual(1, len([ x for x in bar.indexes if x[0] == 'baz_bin'
                                ]))

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_secondary_index_query(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        results = bucket.get_index('field1_bin', 'val2')
        self.assertEqual(1, len(results))
        self.assertEqual(o2.key, str(results[0]))
        results = bucket.get_index('field1_bin', 'val2', 'val4')
        vals = set([ str(key) for key in results ])
        self.assertEqual(3, len(results))
        self.assertEqual(set([o2.key, o3.key, o4.key]), vals)
        results = bucket.get_index('field2_int', 1002)
        self.assertEqual(1, len(results))
        self.assertEqual(o2.key, str(results[0]))
        results = bucket.get_index('field2_int', 1002, 1004)
        vals = set([ str(key) for key in results ])
        self.assertEqual(3, len(results))
        self.assertEqual(set([o2.key, o3.key, o4.key]), vals)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_secondary_index_invalid_name(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket = self.client.bucket(self.bucket_name)
        with self.assertRaises(RiakError):
            bucket.new('k', 'a').add_index('field1', 'value1')

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_set_index(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket = self.client.bucket(self.bucket_name)
        obj = bucket.new('bar', 1)
        obj.set_index('bar_int', 1)
        obj.set_index('bar2_int', 1)
        self.assertEqual(2, len(obj.indexes))
        self.assertEqual(set((('bar_int', 1), ('bar2_int', 1))), obj.indexes)
        obj.set_index('bar_int', 3)
        self.assertEqual(2, len(obj.indexes))
        self.assertEqual(set((('bar_int', 3), ('bar2_int', 1))), obj.indexes)
        obj.set_index('bar2_int', 10)
        self.assertEqual(set((('bar_int', 3), ('bar2_int', 10))), obj.indexes)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_stream_index(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        keys = []
        for entries in bucket.stream_index('field1_bin', 'val1', 'val3'):
            keys.extend(entries)

        self.assertEqual(sorted([o1.key, o2.key, o3.key]), sorted(keys))

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_return_terms(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        pairs = bucket.get_index('field1_bin', 'val2', 'val4', return_terms=True)
        self.assertEqual([('val2', o2.key),
         (
          'val3', o3.key),
         (
          'val4', o4.key)], sorted(pairs))
        spairs = []
        for chunk in bucket.stream_index('field2_int', 1002, 1004, return_terms=True):
            spairs.extend(chunk)

        self.assertEqual([(1002, o2.key), (1003, o3.key), (1004, o4.key)], sorted(spairs))

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_pagination(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        results = bucket.get_index('field1_bin', 'val0', 'val5', max_results=2)
        self.assertLessEqual(2, len(results))
        self.assertEqual([o1.key, o2.key], results)
        self.assertIsNotNone(results.continuation)
        self.assertTrue(results.has_next_page())
        page2 = results.next_page()
        self.assertLessEqual(2, len(page2))
        self.assertEqual([o3.key, o4.key], page2)
        presults = []
        pagecount = 0
        for page in bucket.paginate_index('field1_bin', 'val0', 'val5', max_results=2):
            pagecount += 1
            presults.extend(page.results)

        self.assertEqual(3, pagecount)
        self.assertEqual([o1.key, o2.key, o3.key, o4.key], presults)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_pagination_return_terms(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        results = bucket.get_index('field1_bin', 'val0', 'val5', max_results=2, return_terms=True)
        self.assertLessEqual(2, len(results))
        self.assertEqual([('val1', o1.key), ('val2', o2.key)], results)
        self.assertIsNotNone(results.continuation)
        self.assertTrue(results.has_next_page())
        page2 = results.next_page()
        self.assertLessEqual(2, len(results))
        self.assertEqual([('val3', o3.key), ('val4', o4.key)], page2)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_pagination_stream(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        stream = bucket.stream_index('field1_bin', 'val0', 'val5', max_results=2)
        results = []
        for result in stream:
            results.extend(result)

        self.assertLessEqual(2, len(results))
        self.assertEqual([o1.key, o2.key], results)
        self.assertIsNotNone(stream.continuation)
        self.assertTrue(stream.has_next_page())
        results = []
        for result in stream.next_page():
            results.extend(result)

        self.assertLessEqual(2, len(results))
        self.assertEqual([o3.key, o4.key], results)
        presults = []
        pagecount = 0
        for page in bucket.paginate_stream_index('field1_bin', 'val0', 'val5', max_results=2):
            pagecount += 1
            for result in page:
                presults.extend(result)

        self.assertEqual(3, pagecount)
        self.assertEqual([o1.key, o2.key, o3.key, o4.key], presults)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_pagination_stream_return_terms(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        stream = bucket.stream_index('field1_bin', 'val0', 'val5', max_results=2, return_terms=True)
        results = []
        for result in stream:
            results.extend(result)

        self.assertLessEqual(2, len(results))
        self.assertEqual([('val1', o1.key), ('val2', o2.key)], results)
        self.assertIsNotNone(stream.continuation)
        self.assertTrue(stream.has_next_page())
        results = []
        for result in stream.next_page():
            results.extend(result)

        self.assertLessEqual(2, len(results))
        self.assertEqual([('val3', o3.key), ('val4', o4.key)], results)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_eq_query_return_terms(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        results = bucket.get_index('field2_int', 1001, return_terms=True)
        self.assertEqual([(1001, o1.key)], results)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_eq_query_stream_return_terms(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        results = []
        for item in bucket.stream_index('field2_int', 1001, return_terms=True):
            results.extend(item)

        self.assertEqual([(1001, o1.key)], results)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_timeout(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        self.assertEqual([o1.key], bucket.get_index('field1_bin', 'val1', timeout='infinity'))

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_regex(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects()
        results = []
        for item in bucket.stream_index('field1_bin', 'val0', 'val5', term_regex='.*l2', return_terms=True):
            results.extend(item)

        self.assertEqual([('val2', o2.key)], results)

    @unittest.skipUnless(RUN_INDEXES, 'RUN_INDEXES is 0')
    def test_index_falsey_endkey_gh378(self):
        if not self.is_2i_supported():
            raise unittest.SkipTest('2I is not supported')
        bucket, o1, o2, o3, o4 = self._create_index_objects(int_sign=-1)
        results = []
        for item in bucket.stream_index('field2_int', -10000, 0):
            results.extend(item)

        self.assertEqual(set([o4.key, o3.key, o2.key, o1.key]), set(results))

    def _create_index_objects(self, int_sign=1):
        """
        Creates a number of index objects to be used in 2i test
        """
        bucket = self.client.bucket(self.bucket_name)
        o1 = bucket.new(self.randname(), 'data1').add_index('field1_bin', 'val1').add_index('field2_int', int_sign * 1001).store()
        o2 = bucket.new(self.randname(), 'data1').add_index('field1_bin', 'val2').add_index('field2_int', int_sign * 1002).store()
        o3 = bucket.new(self.randname(), 'data1').add_index('field1_bin', 'val3').add_index('field2_int', int_sign * 1003).store()
        o4 = bucket.new(self.randname(), 'data1').add_index('field1_bin', 'val4').add_index('field2_int', int_sign * 1004).store()
        return (
         bucket, o1, o2, o3, o4)