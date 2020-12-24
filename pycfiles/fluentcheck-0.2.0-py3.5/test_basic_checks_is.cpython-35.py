# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_basic_checks_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 580 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError

class TestIsBasicChecks(unittest.TestCase):

    def test_is_none_pass(self):
        self.assertIsInstance(Is(None).none, Is)

    def test_is_none_fail(self):
        with self.assertRaises(CheckError):
            Is('I am not none').none

    def test_is_not_none_pass(self):
        self.assertIsInstance(Is('I am not none').not_none, Is)

    def test_is_not_none_fail(self):
        with self.assertRaises(CheckError):
            Is(None).not_none