# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/lib/testcase.py
# Compiled at: 2010-06-19 04:55:18
"""The idea is to improve Python's unittest.TestCase class with a more pythonic
API and some convenience functionality."""
from unittest import TestCase
from trac_captcha.lib.simple_super import SuperProxy
__all__ = [
 'PythonicTestCase']

class PythonicTestCase(TestCase):
    super = SuperProxy()

    def assert_raises(self, exception_type, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
        except exception_type as e:
            return e

        self.assertRaises(exception_type, lambda : None)

    def assert_false(self, actual, msg=None):
        self.assertEquals(False, actual, msg=msg)

    def assert_true(self, actual, msg=None):
        self.assertEquals(True, actual, msg=msg)

    def assert_trueish(self, actual, msg=None):
        self.assertTrue(actual, msg=msg)

    def assert_none(self, actual, msg=None):
        self.assertEquals(None, actual, msg=msg)
        return

    def assert_not_none(self, actual, msg=None):
        self.assertNotEquals(None, actual, msg=msg)
        return

    def assert_equals(self, expected, actual, msg=None):
        self.assertEquals(expected, actual, msg=msg)

    def assert_not_equals(self, expected, actual, msg=None):
        self.assertNotEquals(expected, actual, msg=msg)

    def assert_almost_equals(self, expected, actual, places=None, msg=None):
        self.assertAlmostEqual(expected, actual, places=places, msg=msg)

    def assert_contains(self, expected_value, actual_iterable, msg=None):
        if expected_value in actual_iterable:
            return
        message = msg or '%s not in %s' % (repr(expected_value), repr(actual_iterable))
        raise self.failureException(message)

    def assert_dict_contains(self, expected_sub_dict, actual_super_dict):
        for key, value in expected_sub_dict.items():
            message = '%s:%s not in %s' % (repr(key), repr(value), repr(actual_super_dict))
            self.assert_contains(key, actual_super_dict, msg=message)
            self.assert_equals(value, actual_super_dict[key], msg=message)