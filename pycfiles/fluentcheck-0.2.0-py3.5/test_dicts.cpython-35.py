# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_check/test_dicts.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1143 bytes
import unittest
from fluentcheck.classes import Check
from fluentcheck.exceptions import CheckError

class TestDictsAssertions(unittest.TestCase):

    def test_is_dict(self):
        res = Check(dict()).is_dict()
        self.assertIsInstance(res, Check)
        try:
            Check(123).is_dict()
            self.fail()
        except CheckError:
            pass

    def test_is_not_dict(self):
        res = Check(set()).is_not_dict()
        self.assertIsInstance(res, Check)
        try:
            Check(dict()).is_not_dict()
            self.fail()
        except CheckError:
            pass

    def test_has_keys(self):
        d = {1: 'one', 2: 'two'}
        res = Check(d).has_keys(1, 2)
        self.assertIsInstance(res, Check)
        try:
            Check(d).has_keys(3, 4)
            self.fail()
        except CheckError:
            pass

    def test_has_not_keys(self):
        d = {1: 'one', 2: 'two'}
        res = Check(d).has_not_keys(3, 4)
        self.assertIsInstance(res, Check)
        try:
            Check(d).has_not_keys(1, 2)
            self.fail()
        except CheckError:
            pass