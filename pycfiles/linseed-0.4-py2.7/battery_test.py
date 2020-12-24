# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/test/battery_test.py
# Compiled at: 2011-05-31 11:44:21
import unittest
from linseed import Batteries

class Test(unittest.TestCase):

    def test_count(self):
        Batteries.count()


class InfoTest(unittest.TestCase):

    def setUp(self):
        self.b = Batteries()

    def test_design_capacity(self):
        for b in self.b:
            x = b.info.design_capacity

    def test_last_full_capacity(self):
        for b in self.b:
            x = b.info.last_full_capacity


class StateTest(unittest.TestCase):

    def setUp(self):
        self.b = Batteries()

    def test_charging_state(self):
        for b in self.b:
            x = b.state.charging_state

    def test_remaining_capacity(self):
        for b in self.b:
            x = b.state.remaining_capacity