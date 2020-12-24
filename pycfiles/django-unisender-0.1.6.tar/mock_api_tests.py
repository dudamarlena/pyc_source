# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/africa/work/python/djnago-unisender/unisender/tests/mock_api_tests.py
# Compiled at: 2014-07-23 09:14:57
import unittest
from unisender.tests.mock_api import unisender_test_api_correct_values

class MockApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = unisender_test_api_correct_values(object)

    def test__all_requirement_fields_present(self):
        kwargs = {'test': 1, 'test_1': 2}
        requirement_fields = [
         'test']
        self.assertIsNone(self.api.all_requirement_fields_present(requirement_fields, kwargs))
        self.assertRaises(NameError, self.api.all_requirement_fields_present, [
         'test_3'], kwargs)

    def test__not_documented_fields_not_present(self):
        kwargs = {'test': 1, 'test_1': 2}
        requirement_fields = [
         'test']
        all_fields = ['test_1']
        self.assertIsNone(self.api.not_documented_fields_not_present(requirement_fields, all_fields, kwargs))
        self.assertRaises(NameError, self.api.not_documented_fields_not_present, all_fields, ['test_3'], kwargs)