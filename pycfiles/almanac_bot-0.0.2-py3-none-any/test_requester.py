# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/test/test_requester.py
# Compiled at: 2015-08-31 22:18:14
import alman, unittest

class TestRequester(unittest.TestCase):
    params = {'a': 1, 
       'b': [
           2, 3]}
    url = 'test_url'


class TestRequesterGetHeadDelete(TestRequester):

    def test_convert_get_params(self):
        url, params = alman.apibits.Requester.prepare_params(self.url, {}, self.params, 'get')
        self.assertNotEqual(url, self.url)
        self.assertIsNone(params)

    def test_convert_delete_params(self):
        url, params = alman.apibits.Requester.prepare_params(self.url, {}, self.params, 'delete')
        self.assertNotEqual(url, self.url)
        self.assertIsNone(params)

    def test_convert_head_params(self):
        url, params = alman.apibits.Requester.prepare_params(self.url, {}, self.params, 'head')
        self.assertNotEqual(url, self.url)
        self.assertIsNone(params)


class TestRequesterPost(TestRequester):

    def setUp(self):
        self.method = 'post'

    def test_convert_post_params(self):
        url, params = alman.apibits.Requester.prepare_params(self.url, {}, self.params, self.method)
        self.assertIsInstance(params, str)


class TestRequesterQuery(TestRequester):

    def test_query_array_join(self):
        data = self.params
        expected = ['a=1', 'b[]=2', 'b[]=3']
        actual = alman.apibits.Requester.query_string(data).split('&')
        for param in actual:
            self.assertIn(param, expected)

    def test_query_array_flat(self):
        data = {'a': 'value'}
        expected = ['a=value']
        self.assertEqual(expected, alman.apibits.Requester.query_array(data))

    def test_query_array_nested(self):
        data = {'a': {'b': {'c': 'cvalue'}}}
        expected = [
         'a[b][c]=cvalue']
        self.assertEqual(expected, alman.apibits.Requester.query_array(data))

    def test_query_array_list(self):
        data = {'a': [1, 2]}
        expected = [
         'a[]=1', 'a[]=2']
        self.assertEqual(expected, alman.apibits.Requester.query_array(data))