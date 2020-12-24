# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qqqfome/test/test_common.py
# Compiled at: 2016-02-11 00:53:11
# Size of source mod 2**32: 1063 bytes
import unittest
from .. import common as c

class CommonFuncTest(unittest.TestCase):

    def test_check_type_success_with_ref_is_a_value(self):
        try:
            c.check_type(1, 'num', 1)
            a = 1
            c.check_type(1, 'num', a)
        except ValueError:
            self.fail('check_type function raise a exception when the check should be success.')

    def test_check_type_success_with_ref_is_a_type(self):
        try:
            c.check_type(1, 'num', int)
        except ValueError:
            self.fail('check_type function raise a exception when the check should be success.')

    def test_check_type_fail_with_ref_is_a_value(self):
        with self.assertRaises(ValueError):
            c.check_type(1, 'string', '')
        with self.assertRaises(ValueError):
            string = ''
            c.check_type(1, 'string', string)

    def test_check_type_fail_with_ref_is_a_type(self):
        with self.assertRaises(ValueError):
            c.check_type(1, 'string', str)