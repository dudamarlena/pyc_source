# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\customcommands\test_validate_cmd_name.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from unittest2 import TestCase
from b3.config import CfgConfigParser
from b3.plugins.customcommands import CustomcommandsPlugin

class Test_validate_cmd_name(TestCase):

    def setUp(self):
        self.conf = CfgConfigParser()
        self.p = CustomcommandsPlugin(Mock(), self.conf)

    def test_None(self):
        self.assertRaises(AssertionError, self.p._validate_cmd_name, None)
        return

    def test_blank(self):
        self.assertRaises(AssertionError, self.p._validate_cmd_name, '  ')

    def test_does_not_start_with_a_letter(self):
        self.assertRaises(ValueError, self.p._validate_cmd_name, '!f00')
        self.assertRaises(ValueError, self.p._validate_cmd_name, '1f00')
        self.assertRaises(ValueError, self.p._validate_cmd_name, '*f00')

    def test_too_short(self):
        self.assertRaises(ValueError, self.p._validate_cmd_name, 'f')

    def test_have_blank(self):
        self.assertRaises(ValueError, self.p._validate_cmd_name, 'ab cd')

    def test_nominal(self):
        try:
            self.p._validate_cmd_name('cookie')
        except (AssertionError, ValueError) as err:
            self.fail('expecting no error, got %r' % err)