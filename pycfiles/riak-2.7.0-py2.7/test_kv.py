# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_kv.py
# Compiled at: 2016-12-12 17:42:39
import copy, os, sys, unittest
from six import string_types, PY2, PY3
from time import sleep
from riak import ConflictError, RiakBucket, RiakError
from riak.resolver import default_resolver, last_written_resolver
from riak.tests import RUN_KV, RUN_RESOLVE, PROTOCOL
from riak.tests.base import IntegrationTestBase
from riak.tests.comparison import Comparison
try:
    import simplejson as json
except ImportError:
    import json

if PY2:
    import cPickle
    test_pickle_dumps = cPickle.dumps
    test_pickle_loads = cPickle.loads
else:
    import pickle
    test_pickle_dumps = pickle.dumps
    test_pickle_loads = pickle.loads
testrun_sibs_bucket = 'sibsbucket'
testrun_props_bucket = 'propsbucket'

def setUpModule():
    if not RUN_KV:
        return
    c = IntegrationTestBase.create_client()
    c.bucket(testrun_sibs_bucket).allow_mult = True
    c.close()


def tearDownModule():
    if not RUN_KV:
        return
    c = IntegrationTestBase.create_client()
    c.bucket(testrun_sibs_bucket).clear_properties()
    c.bucket(testrun_props_bucket).clear_properties()
    c.close()


class NotJsonSerializable(object):

    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = kwargs

    def __eq__(self, other):
        if len(self.args) != len(other.args):
            return False
        if len(self.kwargs) != len(other.kwargs):
            return False
        for name, value in self.kwargs.items():
            if other.kwargs[name] != value:
                return False

        value1_args = copy.copy(self.args)
        value2_args = copy.copy(other.args)
        value1_args.sort()
        value2_args.sort()
        for i in range(len(value1_args)):
            if value1_args[i] != value2_args[i]:
                return False

        return True


@unittest.skipUnless(RUN_KV, 'RUN_KV is 0')
class BasicKVTests(IntegrationTestBase, unittest.TestCase, Comparison):

    def test_no_returnbody(self):
        bucket = self.client.bucket(self.bucket_name)
        o = bucket.new(self.key_name, 'bar').store(return_body=False)
        self.assertEqual(o.vclock, None)
        return

    @unittest.skipUnless(PROTOCOL == 'pbc', 'Only available on pbc')
    def test_get_no_returnbody(self):
        bucket = self.client.bucket(self.bucket_name)
        o = bucket.new(self.key_name, "Ain't no body")
        o.store()
        stored_object = bucket.get(self.key_name, head_only=True)
        self.assertFalse(stored_object.data)
        list_of_objects = bucket.multiget([self.key_name], head_only=True)
        for stored_object in list_of_objects:
            self.assertFalse(stored_object.data)

    def test_many_link_headers_should_work_fine(self):
        bucket = self.client.bucket(self.bucket_name)
        o = bucket.new('lots_of_links', "My god, it's full of links!")
        for i in range(0, 300):
            link = (
             'other', 'key%d' % i, 'next')
            o.add_link(link)

        o.store()
        stored_object = bucket.get('lots_of_links')
        self.assertEqual(len(stored_object.links), 300)

    def test_is_alive(self):
        self.assertTrue(self.client.is_alive())

    def test_store_and_get(self):
        bucket = self.client.bucket(self.bucket_name)
        rand = self.randint()
        obj = bucket.new('foo', rand)
        obj.store()
        obj = bucket.get('foo')
        self.assertTrue(obj.exists)
        self.assertEqual(obj.bucket.name, self.bucket_name)
        self.assertEqual(obj.key, 'foo')
        self.assertEqual(obj.data, rand)
        if PY2:
            self.client.bucket(unicode(self.bucket_name))
        else:
            self.client.bucket(self.bucket_name)
        if PY2:
            self.assertRaises(TypeError, self.client.bucket, 'búcket')
            self.assertRaises(TypeError, self.client.bucket, 'búcket')
        else:
            self.client.bucket('búcket')
            self.client.bucket('búcket')
        bucket.get('foo')
        if PY2:
            self.assertRaises(TypeError, bucket.get, 'føø')
            self.assertRaises(TypeError, bucket.get, 'føø')
            self.assertRaises(TypeError, bucket.new, 'foo', 'éå')
            self.assertRaises(TypeError, bucket.new, 'foo', 'éå')
            self.assertRaises(TypeError, bucket.new, 'foo', 'éå')
            self.assertRaises(TypeError, bucket.new, 'foo', 'éå')
        else:
            bucket.get('føø')
            bucket.get('føø')
            bucket.new('foo', 'éå')
            bucket.new('foo', 'éå')
            bucket.new('foo', 'éå')
            bucket.new('foo', 'éå')
        obj2 = bucket.new('baz', rand, 'application/json')
        obj2.charset = 'UTF-8'
        obj2.store()
        obj2 = bucket.get('baz')
        self.assertEqual(obj2.data, rand)

    def test_store_obj_with_unicode(self):
        bucket = self.client.bucket(self.bucket_name)
        data = {'føø': 'éå'}
        obj = bucket.new('foo', data)
        obj.store()
        obj = bucket.get('foo')
        self.assertEqual(obj.data, data)

    def test_store_unicode_string(self):
        bucket = self.client.bucket(self.bucket_name)
        data = 'some unicode data: Æ'
        obj = bucket.new(self.key_name, encoded_data=data.encode('utf-8'), content_type='text/plain')
        obj.charset = 'utf-8'
        obj.store()
        obj2 = bucket.get(self.key_name)
        self.assertEqual(data, obj2.encoded_data.decode('utf-8'))

    def test_string_bucket_name(self):
        for bad in (12345, True, None, {}, []):
            with self.assert_raises_regex(TypeError, 'must be a string'):
                self.client.bucket(bad)
            with self.assert_raises_regex(TypeError, 'must be a string'):
                RiakBucket(self.client, bad, None)

        if PY2:
            with self.assert_raises_regex(TypeError, 'Unicode bucket names are not supported'):
                self.client.bucket('føø')
        else:
            self.client.bucket('føø')
        self.client.bucket('ASCII')
        return

    def test_generate_key(self):
        bucket = self.client.bucket(self.bucket_name)
        o = bucket.new(None, data={})
        self.assertIsNone(o.key)
        o.store()
        self.assertIsNotNone(o.key)
        self.assertNotIn('/', o.key)
        existing_keys = bucket.get_keys()
        self.assertEqual(len(existing_keys), 1)
        return

    def maybe_store_keys(self):
        skey = 'rkb-init'
        bucket = self.client.bucket('random_key_bucket')
        sobj = bucket.get(skey)
        if sobj.exists:
            return
        else:
            for key in range(1, 1000):
                o = bucket.new(None, data={})
                o.store()

            o = bucket.new(skey, data={})
            o.store()
            return

    def test_stream_keys(self):
        self.maybe_store_keys()
        bucket = self.client.bucket('random_key_bucket')
        regular_keys = bucket.get_keys()
        self.assertNotEqual(len(regular_keys), 0)
        streamed_keys = []
        for keylist in bucket.stream_keys():
            self.assertNotEqual([], keylist)
            for key in keylist:
                self.assertIsInstance(key, string_types)

            streamed_keys += keylist

        self.assertEqual(sorted(regular_keys), sorted(streamed_keys))

    def test_stream_keys_timeout(self):
        self.maybe_store_keys()
        bucket = self.client.bucket('random_key_bucket')
        streamed_keys = []
        with self.assertRaises(RiakError):
            for keylist in self.client.stream_keys(bucket, timeout=1):
                self.assertNotEqual([], keylist)
                for key in keylist:
                    self.assertIsInstance(key, string_types)

                streamed_keys += keylist

    def test_stream_keys_abort(self):
        self.maybe_store_keys()
        bucket = self.client.bucket('random_key_bucket')
        regular_keys = bucket.get_keys()
        self.assertNotEqual(len(regular_keys), 0)
        try:
            for keylist in bucket.stream_keys():
                raise RuntimeError('abort')

        except RuntimeError:
            pass

        robj = bucket.get(regular_keys[0])
        self.assertEqual(len(robj.siblings), 1)
        self.assertEqual(True, robj.exists)

    def test_bad_key(self):
        bucket = self.client.bucket(self.bucket_name)
        obj = bucket.new()
        with self.assertRaises(TypeError):
            bucket.get(None)
        with self.assertRaises(TypeError):
            self.client.get(obj)
        with self.assertRaises(TypeError):
            bucket.get(1)
        return

    def test_binary_store_and_get(self):
        bucket = self.client.bucket(self.bucket_name)
        rand = str(self.randint())
        if PY2:
            rand = bytes(rand)
        else:
            rand = bytes(rand, 'utf-8')
        obj = bucket.new(self.key_name, encoded_data=rand, content_type='text/plain')
        obj.store()
        obj = bucket.get(self.key_name)
        self.assertTrue(obj.exists)
        self.assertEqual(obj.encoded_data, rand)
        data = [
         self.randint(), self.randint(), self.randint()]
        key2 = self.randname()
        obj = bucket.new(key2, data)
        obj.store()
        obj = bucket.get(key2)
        self.assertEqual(data, json.loads(obj.encoded_data.decode()))

    def test_blank_binary_204(self):
        bucket = self.client.bucket(self.bucket_name)
        empty = ''
        if PY2:
            empty = bytes(empty)
        else:
            empty = bytes(empty, 'utf-8')
        obj = bucket.new('foo2', encoded_data=empty, content_type='text/plain')
        obj.store()
        obj = bucket.get('foo2')
        self.assertTrue(obj.exists)
        self.assertEqual(obj.encoded_data, empty)

    def test_custom_bucket_encoder_decoder(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.set_encoder('application/x-pickle', test_pickle_dumps)
        bucket.set_decoder('application/x-pickle', test_pickle_loads)
        data = {'array': [1, 2, 3], 'badforjson': NotJsonSerializable(1, 3)}
        obj = bucket.new(self.key_name, data, 'application/x-pickle')
        obj.store()
        obj2 = bucket.get(self.key_name)
        self.assertEqual(data, obj2.data)

    def test_custom_client_encoder_decoder(self):
        bucket = self.client.bucket(self.bucket_name)
        self.client.set_encoder('application/x-pickle', test_pickle_dumps)
        self.client.set_decoder('application/x-pickle', test_pickle_loads)
        data = {'array': [1, 2, 3], 'badforjson': NotJsonSerializable(1, 3)}
        obj = bucket.new(self.key_name, data, 'application/x-pickle')
        obj.store()
        obj2 = bucket.get(self.key_name)
        self.assertEqual(data, obj2.data)

    def test_unknown_content_type_encoder_decoder(self):
        bucket = self.client.bucket(self.bucket_name)
        data = 'some funny data'
        if PY3:
            data = data.encode()
        obj = bucket.new(self.key_name, encoded_data=data, content_type='application/x-frobnicator')
        obj.store()
        obj2 = bucket.get(self.key_name)
        self.assertEqual(data, obj2.encoded_data)

    def test_text_plain_encoder_decoder(self):
        bucket = self.client.bucket(self.bucket_name)
        data = 'some funny data'
        obj = bucket.new(self.key_name, data, content_type='text/plain')
        obj.store()
        obj2 = bucket.get(self.key_name)
        self.assertEqual(data, obj2.data)

    def test_missing_object(self):
        bucket = self.client.bucket(self.bucket_name)
        obj = bucket.get(self.key_name)
        self.assertFalse(obj.exists)
        self.assertIsNone(obj.data)

    def test_delete(self):
        bucket = self.client.bucket(self.bucket_name)
        rand = self.randint()
        obj = bucket.new(self.key_name, rand)
        obj.store()
        obj = bucket.get(self.key_name)
        self.assertTrue(obj.exists)
        obj.delete()
        obj.reload()
        self.assertFalse(obj.exists)

    def test_bucket_delete(self):
        bucket = self.client.bucket(self.bucket_name)
        rand = self.randint()
        obj = bucket.new(self.key_name, rand)
        obj.store()
        bucket.delete(self.key_name)
        obj.reload()
        self.assertFalse(obj.exists)

    def test_set_bucket_properties(self):
        bucket = self.client.bucket(testrun_props_bucket)
        bucket.allow_mult = True
        bucket.n_val = 1
        c2 = self.create_client()
        bucket2 = c2.bucket(testrun_props_bucket)
        self.assertTrue(bucket2.allow_mult)
        self.assertEqual(bucket2.n_val, 1)
        bucket.set_properties({'allow_mult': False, 'n_val': 2})
        c3 = self.create_client()
        bucket3 = c3.bucket(testrun_props_bucket)
        self.assertFalse(bucket3.allow_mult)
        self.assertEqual(bucket3.n_val, 2)
        c2.close()
        c3.close()

    def test_if_none_match(self):
        bucket = self.client.bucket(self.bucket_name)
        obj = bucket.get(self.key_name)
        obj.delete()
        obj.reload()
        self.assertFalse(obj.exists)
        obj.data = ['first store']
        obj.content_type = 'application/json'
        obj.store()
        obj.data = [
         'second store']
        with self.assertRaises(Exception):
            obj.store(if_none_match=True)

    def test_siblings(self):
        bucket = self.client.bucket(testrun_sibs_bucket)
        obj = bucket.get(self.key_name)
        bucket.allow_mult = True
        obj.data = 'start'
        obj.content_type = 'text/plain'
        obj.store()
        vals = set(self.generate_siblings(obj, count=5))
        obj = bucket.get(self.key_name)
        self.assertEqual(len(obj.siblings), 5)
        with self.assertRaises(ConflictError):
            obj.data
        vals2 = set([ sibling.data for sibling in obj.siblings ])
        self.assertEqual(vals, vals2)
        resolved_sibling = obj.siblings[3]
        obj.siblings = [resolved_sibling]
        self.assertEqual(len(obj.siblings), 1)
        obj.store()
        self.assertEqual(len(obj.siblings), 1)
        self.assertEqual(obj.data, resolved_sibling.data)

    @unittest.skipUnless(RUN_RESOLVE, 'RUN_RESOLVE is 0')
    def test_resolution(self):
        bucket = self.client.bucket(testrun_sibs_bucket)
        obj = bucket.get(self.key_name)
        bucket.allow_mult = True
        obj.data = 'start'
        obj.content_type = 'text/plain'
        obj.store()
        vals = self.generate_siblings(obj, count=5, delay=1.01)
        obj = bucket.get(self.key_name)
        obj.reload()
        self.assertEqual(len(obj.siblings), 5)
        self.client.resolver = last_written_resolver
        obj.reload()
        self.assertEqual(obj.resolver, last_written_resolver)
        self.assertEqual(1, len(obj.siblings))
        self.assertEqual(obj.data, vals[(-1)])
        bucket.resolver = default_resolver
        obj.reload()
        self.assertEqual(obj.resolver, default_resolver)
        self.assertEqual(len(obj.siblings), 5)

        def max_value_resolver(obj):
            obj.siblings = [
             max(obj.siblings, key=lambda s: s.data)]

        obj.resolver = max_value_resolver
        obj.reload()
        self.assertEqual(obj.resolver, max_value_resolver)
        self.assertEqual(obj.data, max(vals))
        obj.resolver = None
        self.assertEqual(obj.resolver, default_resolver)
        bucket.resolver = None
        self.assertEqual(obj.resolver, last_written_resolver)
        self.client.resolver = None
        self.assertEqual(obj.resolver, default_resolver)
        self.assertEqual(bucket.resolver, default_resolver)
        self.assertEqual(self.client.resolver, default_resolver)
        return

    @unittest.skipUnless(RUN_RESOLVE, 'RUN_RESOLVE is 0')
    def test_resolution_default(self):
        bucket = self.client.bucket(testrun_sibs_bucket)
        self.assertEqual(self.client.resolver, default_resolver)
        self.assertEqual(bucket.resolver, default_resolver)

    def test_tombstone_siblings(self):
        bucket = self.client.bucket(testrun_sibs_bucket)
        obj = bucket.get(self.key_name)
        bucket.allow_mult = True
        obj.data = 'start'
        obj.content_type = 'text/plain'
        obj.store(return_body=True)
        obj.delete()
        vals = set(self.generate_siblings(obj, count=4))
        obj = bucket.get(self.key_name)
        siblen = len(obj.siblings)
        self.assertTrue(siblen == 4 or siblen == 5)
        non_tombstones = 0
        for sib in obj.siblings:
            if sib.exists:
                non_tombstones += 1
            self.assertTrue(not sib.exists or sib.data in vals)

        self.assertEqual(non_tombstones, 4)

    def test_store_of_missing_object(self):
        bucket = self.client.bucket(self.bucket_name)
        o = bucket.get(self.key_name)
        self.assertEqual(o.exists, False)
        o.data = {'foo': 'bar'}
        o.content_type = 'application/json'
        o = o.store()
        self.assertEqual(o.data, {'foo': 'bar'})
        self.assertEqual(o.content_type, 'application/json')
        o.delete()
        o = bucket.get(self.randname())
        self.assertEqual(o.exists, False)
        if PY2:
            o.encoded_data = '1234567890'
        else:
            o.encoded_data = ('1234567890').encode()
        o.content_type = 'application/octet-stream'
        o = o.store()
        if PY2:
            self.assertEqual(o.encoded_data, '1234567890')
        else:
            self.assertEqual(o.encoded_data, ('1234567890').encode())
        self.assertEqual(o.content_type, 'application/octet-stream')
        o.delete()

    def test_store_metadata(self):
        bucket = self.client.bucket(self.bucket_name)
        rand = self.randint()
        obj = bucket.new(self.key_name, rand)
        obj.usermeta = {'custom': 'some metadata'}
        obj.store()
        obj = bucket.get(self.key_name)
        self.assertEqual('some metadata', obj.usermeta['custom'])

    def test_list_buckets(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new('one', {'foo': 'one', 'bar': 'red'}).store()
        buckets = self.client.get_buckets()
        self.assertTrue(self.bucket_name in [ x.name for x in buckets ])

    def test_stream_buckets(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new(self.key_name, data={'foo': 'one', 'bar': 'baz'}).store()
        buckets = []
        for bucket_list in self.client.stream_buckets():
            buckets.extend(bucket_list)

        self.assertTrue(self.bucket_name in [ x.name for x in buckets ])

    def test_stream_buckets_abort(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new(self.key_name, data={'foo': 'one', 'bar': 'baz'}).store()
        try:
            for bucket_list in self.client.stream_buckets():
                raise RuntimeError('abort')

        except RuntimeError:
            pass

        robj = bucket.get(self.key_name)
        self.assertTrue(robj.exists)
        self.assertEqual(len(robj.siblings), 1)

    def test_get_params(self):
        bucket = self.client.bucket(self.bucket_name)
        bucket.new(self.key_name, data={'foo': 'one', 'bar': 'baz'}).store()
        bucket.get(self.key_name, basic_quorum=False)
        bucket.get(self.key_name, basic_quorum=True)
        bucket.get(self.key_name, notfound_ok=True)
        bucket.get(self.key_name, notfound_ok=False)
        missing = bucket.get('missing-key', notfound_ok=True, basic_quorum=True)
        self.assertFalse(missing.exists)

    def test_preflist(self):
        nodes = [
         'riak@127.0.0.1', 'dev1@127.0.0.1']
        bucket = self.client.bucket(self.bucket_name)
        bucket.new(self.key_name, data={'foo': 'one', 'bar': 'baz'}).store()
        try:
            preflist = bucket.get_preflist(self.key_name)
            preflist2 = self.client.get_preflist(bucket, self.key_name)
            for pref in (preflist, preflist2):
                self.assertEqual(len(pref), 3)
                self.assertIn(pref[0]['node'], nodes)
                [ self.assertTrue(node['primary']) for node in pref ]

        except NotImplementedError as e:
            raise unittest.SkipTest(e)

    def generate_siblings(self, original, count=5, delay=None):
        vals = []
        for _ in range(count):
            while True:
                randval = str(self.randint())
                if randval not in vals:
                    break

            other_obj = original.bucket.new(key=original.key, data=randval, content_type='text/plain')
            other_obj.vclock = original.vclock
            other_obj.store()
            vals.append(randval)
            if delay:
                sleep(delay)

        return vals


@unittest.skipUnless(RUN_KV, 'RUN_KV is 0')
class BucketPropsTest(IntegrationTestBase, unittest.TestCase):

    def test_rw_settings(self):
        bucket = self.client.bucket(testrun_props_bucket)
        self.assertEqual(bucket.r, 'quorum')
        self.assertEqual(bucket.w, 'quorum')
        self.assertEqual(bucket.dw, 'quorum')
        self.assertEqual(bucket.rw, 'quorum')
        bucket.w = 1
        self.assertEqual(bucket.w, 1)
        bucket.r = 'quorum'
        self.assertEqual(bucket.r, 'quorum')
        bucket.dw = 'all'
        self.assertEqual(bucket.dw, 'all')
        bucket.rw = 'one'
        self.assertEqual(bucket.rw, 'one')
        bucket.set_properties({'w': 'quorum', 'r': 'quorum', 
           'dw': 'quorum', 
           'rw': 'quorum'})
        bucket.clear_properties()

    def test_primary_quora(self):
        bucket = self.client.bucket(testrun_props_bucket)
        self.assertEqual(bucket.pr, 0)
        self.assertEqual(bucket.pw, 0)
        bucket.pr = 1
        self.assertEqual(bucket.pr, 1)
        bucket.pw = 'quorum'
        self.assertEqual(bucket.pw, 'quorum')
        bucket.set_properties({'pr': 0, 'pw': 0})
        bucket.clear_properties()

    def test_clear_bucket_properties(self):
        bucket = self.client.bucket(testrun_props_bucket)
        bucket.allow_mult = True
        self.assertTrue(bucket.allow_mult)
        bucket.n_val = 1
        self.assertEqual(bucket.n_val, 1)
        self.assertTrue(bucket.clear_properties())
        self.assertFalse(bucket.allow_mult)
        self.assertEqual(bucket.n_val, 3)


@unittest.skipUnless(RUN_KV, 'RUN_KV is 0')
class KVFileTests(IntegrationTestBase, unittest.TestCase):

    def test_store_binary_object_from_file(self):
        bucket = self.client.bucket(self.bucket_name)
        obj = bucket.new_from_file(self.key_name, __file__)
        obj.store()
        obj = bucket.get(self.key_name)
        self.assertNotEqual(obj.encoded_data, None)
        is_win32 = sys.platform == 'win32'
        self.assertTrue(obj.content_type == 'text/x-python' or is_win32 and obj.content_type == 'text/plain' or obj.content_type == 'application/x-python-code')
        return

    def test_store_binary_object_from_file_should_use_default_mimetype(self):
        bucket = self.client.bucket(self.bucket_name)
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'README.md')
        obj = bucket.new_from_file(self.key_name, filepath)
        obj.store()
        obj = bucket.get(self.key_name)
        self.assertEqual(obj.content_type, 'application/octet-stream')

    def test_store_binary_object_from_file_should_fail_if_file_not_found(self):
        bucket = self.client.bucket(self.bucket_name)
        with self.assertRaises(IOError):
            bucket.new_from_file(self.key_name, 'FILE_NOT_FOUND')
        obj = bucket.get(self.key_name)
        self.assertFalse(obj.exists)


@unittest.skipUnless(RUN_KV, 'RUN_KV is 0')
class CounterTests(IntegrationTestBase, unittest.TestCase):

    def test_counter_requires_allow_mult(self):
        bucket = self.client.bucket(self.bucket_name)
        if bucket.allow_mult:
            bucket.allow_mult = False
        self.assertFalse(bucket.allow_mult)
        with self.assertRaises(Exception):
            bucket.update_counter(self.key_name, 10)

    def test_counter_ops(self):
        bucket = self.client.bucket(testrun_sibs_bucket)
        self.assertTrue(bucket.allow_mult)
        self.assertEqual(None, bucket.get_counter(self.key_name))
        bucket.update_counter(self.key_name, 10)
        self.assertEqual(10, bucket.get_counter(self.key_name))
        self.assertEqual(15, bucket.update_counter(self.key_name, 5, returnvalue=True))
        self.assertEqual(10, bucket.update_counter(self.key_name, -5, returnvalue=True))
        return