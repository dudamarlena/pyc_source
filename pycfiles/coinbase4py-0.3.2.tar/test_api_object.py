# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/shanedasilva/src/ghc/coinbase/coinbase-python/tests/test_api_object.py
# Compiled at: 2018-01-17 19:23:46
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import copy, json, six, unittest2, warnings
from coinbase.wallet.model import APIObject
from coinbase.wallet.model import new_api_object
api_key = b'fakeapikey'
api_secret = b'fakeapisecret'
warnings.showwarning = lambda *a, **k: None
simple_data = {b'str': b'bar', 
   b'foo': b'bar', 
   b'int': 21, 
   b'float': 21.0, 
   b'bool': False, 
   b'none': None, 
   b'list': [
           1, 2, 3], 
   b'resource': b'foo', 
   b'obj': {b'str': b'bar1', 
            b'foo': b'bar', 
            b'obj': {b'str': b'bar2'}}, 
   b'list_of_objs': [{b'str': b'one'}, {b'str': b'two'}, {b'str': b'three'}]}

class TestNewApiObject(unittest2.TestCase):

    def test_new_api_object(self):
        api_client = lambda x: x
        obj = new_api_object(api_client, simple_data)
        self.assertIsInstance(obj, APIObject)
        self.assertIsNone(obj.response)
        self.assertIsNone(obj.pagination)
        self.assertIsNone(obj.warnings)
        response = lambda x: x
        pagination = lambda x: x
        warnings = lambda x: x
        obj = new_api_object(api_client, simple_data, response=response, pagination=pagination, warnings=warnings)
        self.assertIs(obj.response, response)
        self.assertIs(obj.pagination, pagination)
        self.assertIs(obj.warnings, warnings)

    def test_new_api_object_uses_cls_if_available(self):
        api_client = lambda x: x

        class Foo(APIObject):
            pass

        obj = new_api_object(api_client, simple_data, cls=Foo)
        self.assertIsInstance(obj, Foo)
        self.assertNotIsInstance(obj.obj, Foo)

    def test_new_api_object_guesses_based_on_resource_field(self):
        api_client = lambda x: x

        class Foo(APIObject):
            pass

        import coinbase.wallet.model
        original = coinbase.wallet.model._resource_to_model
        coinbase.wallet.model._resource_to_model = {b'foo': Foo}
        obj = new_api_object(api_client, simple_data)
        self.assertIsInstance(obj, Foo)
        coinbase.wallet.model._resource_to_model = original

    def test_new_api_object_guesses_based_on_keys(self):
        api_client = lambda x: x

        class Foo(APIObject):
            pass

        import coinbase.wallet.model
        original = coinbase.wallet.model._obj_keys_to_model
        coinbase.wallet.model._obj_keys_to_model = {frozenset(('str', 'foo')): Foo}
        simple_obj = new_api_object(api_client, simple_data)
        self.assertIsInstance(simple_obj, Foo)
        self.assertIsInstance(simple_obj[b'obj'], Foo)
        for obj in simple_obj[b'list_of_objs']:
            self.assertNotIsInstance(obj, Foo)

        coinbase.wallet.model._obj_keys_to_model = original

    def test_new_api_object_transforms_types_appropriately(self):
        api_client = lambda x: x
        simple_obj = new_api_object(api_client, simple_data)
        self.assertIsInstance(simple_data[b'obj'], dict)
        self.assertIsInstance(simple_obj[b'obj'], APIObject)
        self.assertIsInstance(simple_data[b'obj'][b'obj'], dict)
        self.assertIsInstance(simple_obj[b'obj'][b'obj'], APIObject)
        self.assertIsInstance(simple_data[b'list_of_objs'], list)
        self.assertIsInstance(simple_obj[b'list_of_objs'], list)
        for item in simple_data[b'list_of_objs']:
            self.assertIsInstance(item, dict)

        for item in simple_obj[b'list_of_objs']:
            self.assertIsInstance(item, APIObject)

        self.assertIsInstance(simple_data[b'str'], six.string_types)
        self.assertIsInstance(simple_obj[b'str'], six.string_types)
        self.assertIsInstance(simple_data[b'int'], int)
        self.assertIsInstance(simple_obj[b'int'], int)
        self.assertIsInstance(simple_data[b'float'], float)
        self.assertIsInstance(simple_obj[b'float'], float)
        self.assertIsInstance(simple_data[b'bool'], bool)
        self.assertIsInstance(simple_obj[b'bool'], bool)
        self.assertIsNone(simple_data[b'none'])
        self.assertIsNone(simple_obj[b'none'])

    def test_new_api_object_preserves_api_client(self):
        api_client = lambda x: x
        simple_obj = new_api_object(api_client, simple_data)
        self.assertIs(simple_obj.api_client, api_client)
        self.assertIs(simple_obj[b'obj'].api_client, api_client)
        for thing in simple_obj[b'list_of_objs']:
            self.assertIs(thing.api_client, api_client)

    def test_attr_access(self):
        api_client = lambda x: x
        simple_obj = new_api_object(api_client, simple_data)
        for key, value in simple_obj.items():
            assert key in simple_obj and hasattr(simple_obj, key)
            assert getattr(simple_obj, key) is simple_obj[key]

        broken_key = b'notindata'
        assert broken_key not in simple_obj
        assert not hasattr(simple_obj, broken_key)
        with self.assertRaises(KeyError):
            simple_obj[broken_key]
        with self.assertRaises(AttributeError):
            getattr(simple_obj, broken_key)
        with self.assertRaises(KeyError):
            del simple_obj[broken_key]
        with self.assertRaises(AttributeError):
            delattr(simple_obj, broken_key)
        data = {b'foo': b'bar'}
        data_obj = new_api_object(None, data)
        assert hasattr(data_obj, b'refresh')
        assert b'refresh' not in data_obj
        with self.assertRaises(KeyError):
            data_obj[b'refresh']
        data_obj._test = True
        self.assertEqual(getattr(data_obj, b'_test', None), True)
        self.assertEqual(data_obj.get(b'_test', None), None)
        data_obj.test = True
        self.assertEqual(getattr(data_obj, b'test', None), True)
        self.assertEqual(data_obj.get(b'test', None), True)
        return

    def test_json_serialization(self):
        api_client = lambda x: x
        simple_obj = new_api_object(api_client, simple_data)
        self.assertEqual(simple_obj, simple_data)
        json_data = json.dumps(simple_data, sort_keys=True)
        json_obj = json.dumps(simple_obj, sort_keys=True)
        self.assertEqual(json_data, json_obj)
        simple_obj2 = new_api_object(api_client, simple_data)
        self.assertEqual(simple_obj, simple_obj2)
        from decimal import Decimal
        broken_obj = new_api_object(api_client, {b'cost': Decimal(b'12.0')})
        self.assertTrue(str(broken_obj).endswith(b'(invalid JSON)'))

    def test_paged_data_value(self):
        api_client = lambda x: x
        data = copy.copy(simple_data)
        data[b'data'] = data.pop(b'list_of_objs')
        simple_obj = new_api_object(api_client, data)
        print(simple_obj)
        self.assertEqual(simple_obj[0], simple_obj[b'data'][0])
        self.assertEqual(simple_obj[::], simple_obj[b'data'])
        self.assertEqual(simple_obj[::-1], simple_obj[b'data'][::-1])
        simple_obj2 = new_api_object(api_client, simple_data)
        with self.assertRaises(KeyError):
            simple_obj2[0]
        return