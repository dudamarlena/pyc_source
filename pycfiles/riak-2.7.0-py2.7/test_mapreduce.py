# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_mapreduce.py
# Compiled at: 2016-12-08 20:11:02
from __future__ import print_function
import unittest
from six import PY2
from riak.mapreduce import RiakMapReduce
from riak import key_filter, RiakError
from riak.tests import RUN_MAPREDUCE, RUN_SECURITY, RUN_YZ
from riak.tests.base import IntegrationTestBase
from riak.tests.test_yokozuna import wait_for_yz_index
from riak.tests.yz_setup import yzSetUp, yzTearDown
testrun_yz_mr = {'btype': 'mr', 'bucket': 'mrbucket', 
   'index': 'mrbucket'}

def setUpModule():
    yzSetUp(testrun_yz_mr)


def tearDownModule():
    yzTearDown(testrun_yz_mr)


@unittest.skipUnless(RUN_MAPREDUCE, 'RUN_MAPREDUCE is 0')
class LinkTests(IntegrationTestBase, unittest.TestCase):

    def test_store_and_get_links(self):
        bucket = self.client.bucket(self.bucket_name)
        if PY2:
            bucket.new(key=self.key_name, encoded_data='2', content_type='application/octet-stream').add_link(bucket.new('foo1')).add_link(bucket.new('foo2'), 'tag').add_link(bucket.new('foo3'), 'tag2!@#%^&*)').store()
        else:
            bucket.new(key=self.key_name, data='2', content_type='application/octet-stream').add_link(bucket.new('foo1')).add_link(bucket.new('foo2'), 'tag').add_link(bucket.new('foo3'), 'tag2!@#%^&*)').store()
        obj = bucket.get(self.key_name)
        links = obj.links
        self.assertEqual(len(links), 3)
        for bucket, key, tag in links:
            if key == 'foo1':
                self.assertEqual(bucket, self.bucket_name)
            elif key == 'foo2':
                self.assertEqual(tag, 'tag')
            elif key == 'foo3':
                self.assertEqual(tag, 'tag2!@#%^&*)')
            else:
                self.assertEqual(key, 'unknown key')

    def test_set_links(self):
        bucket = self.client.bucket(self.bucket_name)
        o = bucket.new(self.key_name, 2)
        o.links = [(self.bucket_name, 'foo1', None),
         (
          self.bucket_name, 'foo2', 'tag'),
         ('bucket', 'foo2', 'tag2')]
        o.store()
        obj = bucket.get(self.key_name)
        links = sorted(obj.links, key=lambda x: x[1])
        self.assertEqual(len(links), 3)
        self.assertEqual(links[0][1], 'foo1')
        self.assertEqual(links[1][1], 'foo2')
        self.assertEqual(links[1][2], 'tag')
        self.assertEqual(links[2][1], 'foo2')
        self.assertEqual(links[2][2], 'tag2')
        return

    @unittest.skipIf(RUN_SECURITY, 'RUN_SECURITY is set')
    def test_link_walking(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).add_link(bucket.new('foo1', 'test1').store()).add_link(bucket.new('foo2', 'test2').store(), 'tag').add_link(bucket.new('foo3', 'test3').store(), 'tag2!@#%^&*)').store()
        obj = bucket.get('foo')
        results = obj.link(self.bucket_name).run()
        self.assertEqual(len(results), 3)
        results = obj.link(self.bucket_name, 'tag').run()
        self.assertEqual(len(results), 1)


@unittest.skipUnless(RUN_MAPREDUCE, 'RUN_MAPREDUCE is 0')
class ErlangMapReduceTests(IntegrationTestBase, unittest.TestCase):

    def test_erlang_map_reduce(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 2).store()
        bucket.new('baz', 4).store()
        result = self.client.add(self.bucket_name, 'foo').add(self.bucket_name, 'bar').add(self.bucket_name, 'baz').map([
         'riak_kv_mapreduce', 'map_object_value']).reduce([
         'riak_kv_mapreduce', 'reduce_set_union']).run()
        self.assertEqual(len(result), 2)

    def test_erlang_map_reduce_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 2).store()
        bucket.new('baz', 4).store()
        result = self.client.add(self.bucket_name, 'foo', bucket_type='no_siblings').add(self.bucket_name, 'bar', bucket_type='no_siblings').add(self.bucket_name, 'baz', bucket_type='no_siblings').map([
         'riak_kv_mapreduce', 'map_object_value']).reduce([
         'riak_kv_mapreduce', 'reduce_set_union']).run()
        self.assertEqual(len(result), 2)

    def test_erlang_source_map_reduce(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        strfun_allowed = True
        result = []
        try:
            result = self.client.add(self.bucket_name, 'foo').add(self.bucket_name, 'bar').add(self.bucket_name, 'baz').map('fun(Object, _KD, _A) ->\n            Value = riak_object:get_value(Object),\n            [Value]\n        end.', {'language': 'erlang'}).run()
        except RiakError as e:
            if e.value.startswith('May have tried'):
                strfun_allowed = False
            else:
                print(('test_erlang_source_map_reduce {}').format(e.value))

        if strfun_allowed:
            self.assertIn('2', result)
            self.assertIn('3', result)
            self.assertIn('4', result)

    def test_erlang_source_map_reduce_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        strfun_allowed = True
        try:
            result = self.client.add(self.bucket_name, 'foo', bucket_type='no_siblings').add(self.bucket_name, 'bar', bucket_type='no_siblings').add(self.bucket_name, 'baz', bucket_type='no_siblings').map('fun(Object, _KD, _A) ->\n            Value = riak_object:get_value(Object),\n            [Value]\n        end.', {'language': 'erlang'}).run()
        except RiakError as e:
            if e.value.startswith('May have tried'):
                strfun_allowed = False

        if strfun_allowed:
            self.assertIn('2', result)
            self.assertIn('3', result)
            self.assertIn('4', result)

    def test_client_exceptional_paths(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 2).store()
        bucket.new('baz', 4).store()
        with self.assertRaises(ValueError):
            mr = self.client.add(self.bucket_name)
            mr.add(self.bucket_name, 'bar')
        with self.assertRaises(ValueError):
            mr = self.client.search(self.bucket_name, 'fleh')
            mr.add(self.bucket_name, 'bar')
        with self.assertRaises(ValueError):
            mr = self.client.search(self.bucket_name, 'fleh')
            mr.add_key_filter('tokenize', '-', 1)


@unittest.skipUnless(RUN_MAPREDUCE, 'RUN_MAPREDUCE is 0')
class JSMapReduceTests(IntegrationTestBase, unittest.TestCase):

    def test_javascript_source_map(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        mr = self.client.add(self.bucket_name, 'foo')
        result = mr.map('function (v) { return [JSON.parse(v.values[0].data)]; }').run()
        self.assertEqual(result, [2])
        mr.map('function (v) { return [JSON.parse(v.values[0].data)]; }')
        if PY2:
            self.assertRaises(TypeError, mr.map, '\n                              function (v) {\n                              /* æ */\n                                return [JSON.parse(v.values[0].data)];\n                              }')
        else:
            mr = self.client.add(self.bucket_name, 'foo')
            result = mr.map('function (v) {\n                      /* æ */\n                        return [JSON.parse(v.values[0].data)];\n                      }').run()
            self.assertEqual(result, [2])
        if PY2:
            self.assertRaises(TypeError, mr.map, 'function (v) {\n                                   /* æ */\n                                   return [JSON.parse(v.values[0].data)];\n                                 }')

    def test_javascript_named_map(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        result = self.client.add(self.bucket_name, 'foo').map('Riak.mapValuesJson').run()
        self.assertEqual(result, [2])

    def test_javascript_named_map_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        result = self.client.add(self.bucket_name, 'foo', bucket_type='no_siblings').map('Riak.mapValuesJson').run()
        self.assertEqual(result, [2])

    def test_javascript_source_map_reduce(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        result = self.client.add(self.bucket_name, 'foo').add(self.bucket_name, 'bar').add(self.bucket_name, 'baz').map('function (v) { return [1]; }').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [3])

    def test_javascript_source_map_reduce_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        result = self.client.add(self.bucket_name, 'foo', bucket_type='no_siblings').add(self.bucket_name, 'bar', bucket_type='no_siblings').add(self.bucket_name, 'baz', bucket_type='no_siblings').map('function (v) { return [1]; }').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [3])

    def test_javascript_named_map_reduce(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        result = self.client.add(self.bucket_name, 'foo').add(self.bucket_name, 'bar').add(self.bucket_name, 'baz').map('Riak.mapValuesJson').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [9])

    def test_javascript_named_map_reduce_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        result = self.client.add(self.bucket_name, 'foo', bucket_type='no_siblings').add(self.bucket_name, 'bar', bucket_type='no_siblings').add(self.bucket_name, 'baz', bucket_type='no_siblings').map('Riak.mapValuesJson').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [9])

    def test_javascript_bucket_map_reduce(self):
        bucket = self.client.bucket('bucket_%s' % self.randint())
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        result = self.client.add(bucket.name).map('Riak.mapValuesJson').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [9])

    def test_javascript_bucket_map_reduceP_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket('bucket_%s' % self.randint())
        bucket.new('foo', 2).store()
        bucket.new('bar', 3).store()
        bucket.new('baz', 4).store()
        result = self.client.add(bucket.name, bucket_type='no_siblings').map('Riak.mapValuesJson').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [9])

    def test_javascript_arg_map_reduce(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        result = self.client.add(self.bucket_name, 'foo', 5).add(self.bucket_name, 'foo', 10).add(self.bucket_name, 'foo', 15).add(self.bucket_name, 'foo', -15).add(self.bucket_name, 'foo', -5).map('function(v, arg) { return [arg]; }').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [10])

    def test_javascript_arg_map_reduce_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        result = self.client.add(self.bucket_name, 'foo', 5, bucket_type='no_siblings').add(self.bucket_name, 'foo', 10, bucket_type='no_siblings').add(self.bucket_name, 'foo', 15, bucket_type='no_siblings').add(self.bucket_name, 'foo', -15, bucket_type='no_siblings').add(self.bucket_name, 'foo', -5, bucket_type='no_siblings').map('function(v, arg) { return [arg]; }').reduce('Riak.reduceSum').run()
        self.assertEqual(result, [10])

    def test_key_filters(self):
        bucket = self.client.bucket('kftest')
        bucket.new('basho-20101215', 1).store()
        bucket.new('google-20110103', 2).store()
        bucket.new('yahoo-20090613', 3).store()
        result = self.client.add('kftest').add_key_filters([
         [
          'tokenize', '-', 2]]).add_key_filter('ends_with', '0613').map('function (v, keydata) { return [v.key]; }').run()
        self.assertEqual(result, ['yahoo-20090613'])

    def test_key_filters_bucket_type(self):
        btype = self.client.bucket_type('no_siblings')
        bucket = btype.bucket('kftest')
        bucket.new('basho-20101215', 1).store()
        bucket.new('google-20110103', 2).store()
        bucket.new('yahoo-20090613', 3).store()
        result = self.client.add('kftest', bucket_type='no_siblings').add_key_filters([
         [
          'tokenize', '-', 2]]).add_key_filter('ends_with', '0613').map('function (v, keydata) { return [v.key]; }').run()
        self.assertEqual(result, ['yahoo-20090613'])

    def test_key_filters_f_chain(self):
        bucket = self.client.bucket('kftest')
        bucket.new('basho-20101215', 1).store()
        bucket.new('google-20110103', 2).store()
        bucket.new('yahoo-20090613', 3).store()
        filters = key_filter.tokenize('-', 1).eq('yahoo') & key_filter.tokenize('-', 2).ends_with('0613')
        result = self.client.add('kftest').add_key_filters(filters).map('function (v, keydata) { return [v.key]; }').run()
        self.assertEqual(result, ['yahoo-20090613'])

    def test_key_filters_with_search_query(self):
        mapreduce = self.client.search('kftest', 'query')
        self.assertRaises(Exception, mapreduce.add_key_filters, [
         [
          'tokenize', '-', 2]])
        self.assertRaises(Exception, mapreduce.add_key_filter, 'ends_with', '0613')

    def test_map_reduce_from_object(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('foo', 2).store()
        obj = bucket.get('foo')
        result = obj.map('Riak.mapValuesJson').run()
        self.assertEqual(result, [2])

    def test_mr_list_add(self):
        bucket = self.client.bucket(self.bucket_name)
        for x in range(20):
            bucket.new('baz' + str(x), 'bazval' + str(x)).store()

        mr = self.client.add(self.bucket_name, [ 'baz' + str(x) for x in range(2, 5)
                                               ])
        results = mr.map_values().run()
        results.sort()
        self.assertEqual(results, [
         '"bazval2"',
         '"bazval3"',
         '"bazval4"'])

    def test_mr_list_add_two_buckets(self):
        bucket = self.client.bucket(self.bucket_name)
        name2 = self.randname()
        for x in range(10):
            bucket.new('foo' + str(x), 'fooval' + str(x)).store()

        bucket = self.client.bucket(name2)
        for x in range(10):
            bucket.new('bar' + str(x), 'barval' + str(x)).store()

        mr = self.client.add(self.bucket_name, [ 'foo' + str(x) for x in range(2, 4)
                                               ])
        mr.add(name2, [ 'bar' + str(x) for x in range(5, 7)
                      ])
        results = mr.map_values().run()
        results.sort()
        self.assertEqual(results, [
         '"barval5"',
         '"barval6"',
         '"fooval2"',
         '"fooval3"'])

    def test_mr_list_add_mix(self):
        bucket = self.client.bucket('bucket_a')
        for x in range(10):
            bucket.new('foo' + str(x), 'fooval' + str(x)).store()

        bucket = self.client.bucket('bucket_b')
        for x in range(10):
            bucket.new('bar' + str(x), 'barval' + str(x)).store()

        mr = self.client.add('bucket_a', [ 'foo' + str(x) for x in range(2, 4)
                                         ])
        mr.add('bucket_b', 'bar9')
        mr.add('bucket_b', 'bar2')
        results = mr.map_values().run()
        results.sort()
        self.assertEqual(results, [
         '"barval2"',
         '"barval9"',
         '"fooval2"',
         '"fooval3"'])

    @unittest.skipUnless(RUN_YZ, 'RUN_YZ is 0')
    def test_mr_search(self):
        """
        Try a successful map/reduce from search results.
        """
        btype = self.client.bucket_type(testrun_yz_mr['btype'])
        bucket = btype.bucket(testrun_yz_mr['bucket'])
        bucket.new('Pebbles', {'name_s': 'Fruity Pebbles', 'maker_s': 'Post', 
           'sugar_i': 9, 
           'calories_i': 110, 
           'fruit_b': True}).store()
        bucket.new('Loops', {'name_s': 'Froot Loops', 'maker_s': "Kellogg's", 
           'sugar_i': 12, 
           'calories_i': 110, 
           'fruit_b': True}).store()
        bucket.new('Charms', {'name_s': 'Lucky Charms', 'maker_s': 'General Mills', 
           'sugar_i': 10, 
           'calories_i': 110, 
           'fruit_b': False}).store()
        bucket.new('Count', {'name_s': 'Count Chocula', 'maker_s': 'General Mills', 
           'sugar_i': 9, 
           'calories_i': 100, 
           'fruit_b': False}).store()
        bucket.new('Crunch', {'name_s': "Cap'n Crunch", 'maker_s': 'Quaker Oats', 
           'sugar_i': 12, 
           'calories_i': 110, 
           'fruit_b': False}).store()
        wait_for_yz_index(bucket, 'Crunch')
        mr = RiakMapReduce(self.client).search(testrun_yz_mr['bucket'], 'fruit_b:false')
        mr.map('function(v) {\n            var solr_doc = JSON.parse(v.values[0].data);\n            return [solr_doc["calories_i"]]; }')
        result = mr.reduce('function(values, arg) ' + '{ return [values.sort()[0]]; }').run()
        self.assertEqual(result, [100])


@unittest.skipUnless(RUN_MAPREDUCE, 'RUN_MAPREDUCE is 0')
class MapReduceAliasTests(IntegrationTestBase, unittest.TestCase):
    """This tests the map reduce aliases"""

    def test_map_values(self):
        bucket = self.client.bucket(self.bucket_name)
        if PY2:
            bucket.new('one', encoded_data='value_1', content_type='text/plain').store()
            bucket.new('two', encoded_data='value_2', content_type='text/plain').store()
        else:
            bucket.new('one', data='value_1', content_type='text/plain').store()
            bucket.new('two', data='value_2', content_type='text/plain').store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values().run()
        result.sort()
        self.assertEqual(result, ['value_1', 'value_2'])

    def test_map_values_json(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data={'val': 'value_1'}).store()
        bucket.new('two', data={'val': 'value_2'}).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().run()
        result.sort(key=lambda x: x['val'])
        self.assertEqual(result, [{'val': 'value_1'}, {'val': 'value_2'}])

    def test_reduce_sum(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_sum().run()
        self.assertEqual(result, [3])

    def test_reduce_min(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_min().run()
        self.assertEqual(result, [1])

    def test_reduce_max(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_max().run()
        self.assertEqual(result, [2])

    def test_reduce_sort(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data='value1').store()
        bucket.new('two', data='value2').store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_sort().run()
        self.assertEqual(result, ['value1', 'value2'])

    def test_reduce_sort_custom(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data='value1').store()
        bucket.new('two', data='value2').store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_sort('function(x,y) {\n           if(x == y) return 0;\n           return x > y ? -1 : 1;\n        }').run()
        self.assertEqual(result, ['value2', 'value1'])

    def test_reduce_numeric_sort(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_numeric_sort().run()
        self.assertEqual(result, [1, 2])

    def test_reduce_limit(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_numeric_sort().reduce_limit(1).run()
        self.assertEqual(result, [1])

    def test_reduce_slice(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        result = mr.map_values_json().reduce_numeric_sort().reduce_slice(1, 2).run()
        self.assertEqual(result, [2])

    def test_filter_not_found(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = self.client.add(self.bucket_name, 'one').add(self.bucket_name, 'two').add(self.bucket_name, self.key_name)
        result = mr.map_values_json().filter_not_found().run()
        self.assertEqual(sorted(result), [1, 2])


@unittest.skipUnless(RUN_MAPREDUCE, 'RUN_MAPREDUCE is 0')
class MapReduceStreamTests(IntegrationTestBase, unittest.TestCase):

    def test_stream_results(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = RiakMapReduce(self.client).add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        mr.map_values_json()
        results = []
        for phase, data in mr.stream():
            results.extend(data)

        self.assertEqual(sorted(results), [1, 2])

    def test_stream_cleanoperationsup(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', data=1).store()
        bucket.new('two', data=2).store()
        mr = RiakMapReduce(self.client).add(self.bucket_name, 'one').add(self.bucket_name, 'two')
        mr.map_values_json()
        try:
            for phase, data in mr.stream():
                raise RuntimeError('woops')

        except RuntimeError:
            pass

        obj = bucket.get('one')
        if PY2:
            self.assertEqual('1', obj.encoded_data)
        else:
            self.assertEqual('1', obj.encoded_data)