# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/tests/test_validators.py
# Compiled at: 2017-10-08 17:55:08
from __future__ import absolute_import, print_function, unicode_literals
from datetime import date, datetime
from unittest import TestCase
from ngen import validators
NOW = datetime.utcnow()
TODAY = date.today()

class ValidatorTests(TestCase):

    def _tester(self, func, expected_successes, expected_failures):
        for value in expected_successes:
            ret = func(value)
            self.assertEqual(ret, value)

        for value in expected_failures:
            self.assertRaises(validators.ValidationError, func, value)

    def test_is_int(self):
        self._tester(validators.is_int, (-1, 0, 1), (
         1.0, b'bar', [], None, {}, set(), True, (), NOW, TODAY))
        return

    def test_is_float(self):
        self._tester(validators.is_float, (0.0, 1.0), (
         1, b'bar', [], None, {}, set(), True, (), NOW, TODAY))
        return

    def test_is_number(self):
        self._tester(validators.is_number, (-1.0, 0, 1), (
         b'bar', [], None, {}, set(), True, (), NOW, TODAY))
        return

    def test_is_char(self):
        self._tester(validators.is_char, ('bar', ), (
         1.0, 1, [], None, {}, set(), True, (), NOW, TODAY))
        return

    def test_is_bool(self):
        self._tester(validators.is_bool, (
         True, False), (
         1.0, b'bar', 1, [], None, {}, set(), (), NOW, TODAY))
        return

    def test_is_set(self):
        self._tester(validators.is_set, (
         set(),), (
         1.0, b'bar', [], None, {}, True, (), NOW, TODAY))
        return

    def test_is_dict(self):
        self._tester(validators.is_dict, ({},), (
         1.0, b'bar', [], None, set(), True, (), NOW, TODAY))
        return

    def test_is_list(self):
        self._tester(validators.is_list, ([], ()), (
         1.0, b'bar', set(), None, {}, True, NOW, TODAY))
        return

    def test_is_datetime(self):
        self._tester(validators.is_datetime, (
         NOW,), (
         1.0, b'bar', set(), None, {}, True, [], (), TODAY))
        return

    def test_is_date(self):
        self._tester(validators.is_date, (
         TODAY,), (
         1.0, b'bar', set(), None, {}, True, NOW, [], ()))
        return

    def test_check_length(self):
        self.assertRaises(validators.ValidationError, validators.check_length, b'a', min_length=3)
        self.assertRaises(validators.ValidationError, validators.check_length, b'ab', min_length=3)
        expected = b'foo'
        ret = validators.check_length(expected, min_length=3, max_length=5)
        self.assertEqual(ret, expected)
        expected += b'b'
        ret = validators.check_length(expected, min_length=3, max_length=5)
        self.assertEqual(ret, expected)
        expected += b'a'
        ret = validators.check_length(expected, min_length=3, max_length=5)
        self.assertEqual(ret, expected)
        self.assertRaises(validators.ValidationError, validators.check_length, b'foobar', min_length=3, max_length=5)