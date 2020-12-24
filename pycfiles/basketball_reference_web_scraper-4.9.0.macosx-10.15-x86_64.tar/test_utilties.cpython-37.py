# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/test_utilties.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 2221 bytes
from unittest import TestCase
from basketball_reference_web_scraper.utilities import str_to_int, str_to_float, merge_two_dicts

class TestStrToInt(TestCase):

    def test_empty_string_is_zero(self):
        self.assertEqual(str_to_int(''), 0)

    def test_whitespace_is_zero(self):
        self.assertEqual(str_to_int('    '), 0)

    def test_stringified_number_is_converted(self):
        self.assertEqual(str_to_int('10'), 10)

    def test_stringified_number_with_leading_whitespace_is_converted(self):
        self.assertEqual(str_to_int('  10'), 10)

    def test_stringified_number_with_trailing_whitespace_is_converted(self):
        self.assertEqual(str_to_int('10    '), 10)

    def test_with_default(self):
        self.assertIsNone(str_to_int('', default=None))


class TestStrToFloat(TestCase):

    def test_empty_string_is_zero(self):
        self.assertEqual(str_to_float(''), 0.0)

    def test_whitespace_is_zero(self):
        self.assertEqual(str_to_float('    '), 0.0)

    def test_stringified_number_is_converted(self):
        self.assertEqual(str_to_float('1.234'), 1.234)

    def test_stringified_number_with_leading_whitespace_is_converted(self):
        self.assertEqual(str_to_float('  1.234'), 1.234)

    def test_stringified_number_with_trailing_whitespace_is_converted(self):
        self.assertEqual(str_to_float('1.234    '), 1.234)

    def test_with_default(self):
        self.assertIsNone(str_to_float('', default=None))


class TestMergeTwoDicts(TestCase):

    def test_merges_two_empty_dicts(self):
        self.assertEqual({}, merge_two_dicts({}, {}))

    def test_merges_empty_dict_with_non_empty_dict(self):
        self.assertEqual({'jae': 'baebae'}, merge_two_dicts({}, {'jae': 'baebae'}))

    def test_merges_non_empty_dict_with_empty_dict(self):
        self.assertEqual({'jae': 'baebae'}, merge_two_dicts({'jae': 'baebae'}, {}))

    def test_merge_non_empty_dicts_with_unique_keys(self):
        self.assertEqual({'jae':'baebae',  'bae':'jadley'}, merge_two_dicts({'jae': 'baebae'}, {'bae': 'jadley'}))

    def test_merge_non_empty_dicts_with_shared_keys(self):
        self.assertEqual({'jae': 'baebae2'}, merge_two_dicts({'jae': 'baebae'}, {'jae': 'baebae2'}))