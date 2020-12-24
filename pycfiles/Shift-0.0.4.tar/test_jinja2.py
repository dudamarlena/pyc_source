# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrew/Documents/repos/Shift/shift/tests/test_jinja2.py
# Compiled at: 2012-07-24 02:21:21
from . import ShiftTestCase
from .. import Shift, BaseTemplate
from ..engines import JinjaTemplate
import unittest

class TestJinja2(ShiftTestCase):

    def on_setup(self):
        pass

    def test_jinja2_will_load(self):
        self.shift


def suite():
    suite = unittest.TestSuite()
    return suite