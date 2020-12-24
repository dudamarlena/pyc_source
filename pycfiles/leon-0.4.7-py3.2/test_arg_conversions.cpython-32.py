# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leon/tests/test_arg_conversions.py
# Compiled at: 2013-05-03 04:49:53
from unittest import TestCase
from leon.arg_conversions import convert_to_type, list_of

class TestArgConversions(TestCase):

    def test_int_by_type(self):
        self.assertEqual(convert_to_type('1', int), 1)

    def test_int_by_default_value(self):
        self.assertEqual(convert_to_type('1', 5), 1)

    def test_list_by_type(self):
        self.assertEqual(convert_to_type('1', list), ['1'])

    def test_list_of_ints(self):
        self.assertEqual(convert_to_type('1', list_of(int)), [1])

    def test_bool(self):
        self.assertTrue(convert_to_type('true', bool))
        self.assertTrue(convert_to_type('on', bool))
        self.assertTrue(convert_to_type('yes', bool))
        self.assertTrue(convert_to_type('1', bool))
        self.assertFalse(convert_to_type('false', bool))
        self.assertFalse(convert_to_type('off', bool))
        self.assertFalse(convert_to_type('no', bool))
        self.assertFalse(convert_to_type('0', bool))

    def test_argument_conversion_bool_wrong_value(self):
        self.assertRaises(Exception, lambda : convert_to_type('X', bool))