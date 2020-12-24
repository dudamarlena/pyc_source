# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_dicts_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1237 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError

class TestIsDictsAssertions(unittest.TestCase):

    def test_is_dict_pass(self):
        obj = dict()
        self.assertIsInstance(Is(obj).dict, Is)

    def test_is_dict_fail(self):
        obj = set()
        with self.assertRaises(CheckError):
            Is(obj).dict

    def test_is_not_dict_pass(self):
        obj = set()
        self.assertIsInstance(Is(obj).not_dict, Is)

    def test_is_not_dict_fail(self):
        obj = dict()
        with self.assertRaises(CheckError):
            Is(obj).not_dict

    def test_is_has_keys_pass(self):
        obj = {1: 'one', 2: 'two'}
        self.assertIsInstance(Is(obj).has_keys(*obj.keys()), Is)

    def test_is_has_keys_fail(self):
        obj = {1: 'one', 2: 'two'}
        with self.assertRaises(CheckError):
            Is(obj).has_keys(1, 3)

    def test_is_has_not_keys_pass(self):
        obj = {1: 'one', 2: 'two'}
        self.assertIsInstance(Is(obj).has_not_keys(7, 3), Is)

    def test_is_has_not_keys_fail(self):
        obj = {1: 'one', 2: 'two'}
        with self.assertRaises(CheckError):
            Is(obj).has_not_keys(*obj.keys())