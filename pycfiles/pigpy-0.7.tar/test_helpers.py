# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgod/Documents/Sandbox/pigpy/tests/test_helpers.py
# Compiled at: 2009-06-10 23:36:17
import sys, os, unittest
from pigpy.reports import Report, Plan
from pigpy.helpers import filter_report

class test_helpers(unittest.TestCase):

    def setUp(self):
        self.report = Report('to_filter', "%(this)s = LOAD 'bears.txt'")

    def test_basic_filter(self):
        basic = Plan(reports=[filter_report(self.report, '$0 == 0')])
        self.assert_('to_filter' in basic.pigfile)
        self.assert_('$0 == 0' in basic.pigfile)