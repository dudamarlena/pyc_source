# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/urltest/tests/utilities.py
# Compiled at: 2009-07-01 11:22:30
"""These tests check some of the helper functions in urltest"""
import unittest
from urltest import _get_method, _get_test_name

class GetMethodTests(unittest.TestCase):

    def test_method_defaults_to_get(self):
        item = {'url': '/', 'code': 200}
        method = _get_method(item)
        self.assertEqual(method, 'get')

    def test_method_can_be_post(self):
        item = {'url': '/', 'method': 'post', 'code': 200}
        method = _get_method(item)
        self.assertEqual(method, 'post')

    def test_method_capitalisation_doesnt_matter(self):
        item = {'url': '/', 'method': 'POST', 'code': 200}
        method = _get_method(item)
        self.assertEqual(method, 'post')
        item = {'url': '/', 'method': 'PoSt', 'code': 200}
        method = _get_method(item)
        self.assertEqual(method, 'post')

    def test_invalid_method_defaults_to_get(self):
        item = {'url': '/', 'method': 'Foo', 'code': 200}
        method = _get_method(item)
        self.assertEqual(method, 'get')


class NameTests(unittest.TestCase):

    def test_get_request_to_root_with_200_code(self):
        item = {'url': '/', 'code': 200}
        test_name = _get_test_name(item)
        self.assertEqual(test_name, 'test_get_request_of_/_returns_200')

    def test_longer_url_with_404(self):
        item = {'url': '/foo/bar', 'code': 404}
        test_name = _get_test_name(item)
        self.assertEqual(test_name, 'test_get_request_of_/foo/bar_returns_404')

    def test_method_name_is_reflected_in_test_name(self):
        item = {'url': '/foo/bar', 'method': 'delete', 'code': 405}
        test_name = _get_test_name(item)
        self.assertEqual(test_name, 'test_delete_request_of_/foo/bar_returns_405')

    def test_method_in_caps_is_lowercased(self):
        item = {'url': '/', 'code': 200, 'method': 'POST'}
        test_name = _get_test_name(item)
        self.assertEqual(test_name, 'test_post_request_of_/_returns_200')


if __name__ == '__main__':
    unittest.main()