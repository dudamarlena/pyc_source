# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/test_assignment.py
# Compiled at: 2018-01-30 16:37:48
from microbus.assignment import BusAssignment
import microbus
from microbus.bus import Bus
import unittest

class BusAssignmentTest(unittest.TestCase):

    def setUp(self):
        self.stop1 = microbus.BusStop('stop1')
        self.stop2 = microbus.BusStop('stop2')
        self.stop3 = microbus.BusStop('stop3')
        self.stops = [self.stop1, self.stop2, self.stop3]
        self.busRoute1 = microbus.BusRoute(self.stops, name='test')
        self.busRoute2 = self.busRoute1[::-1]
        self.bus = Bus(keep_prev=1)

    def test__contains(self):
        assignment = BusAssignment(self.bus, self.busRoute1)
        self.assertTrue(self.bus in assignment)
        self.assertTrue(self.busRoute1 in assignment)
        self.assertTrue(self.busRoute1[1:] in assignment)
        self.assertTrue(self.busRoute1[2:] in assignment)
        self.assertTrue(self.stop1 in assignment)
        self.assertTrue(self.stop2 in assignment)
        self.assertTrue(self.stop3 in assignment)
        self.assertFalse(microbus.BusStop('bla') in assignment)
        self.assertFalse(self.busRoute1[::-1] in assignment)
        self.assertFalse(self.busRoute1[::-1][1:] in assignment)

    def test_finished(self):
        assignment = BusAssignment(self.bus, self.busRoute1)
        self.assertFalse(assignment.finished)
        assignment()
        self.assertTrue(assignment.finished)

    def test_call(self):
        assignment = BusAssignment(self.bus, self.busRoute1)
        assignment()
        self.assertTrue(self.busRoute1 in self.bus.prev_routes)
        self.assertEqual(1, self.bus.completed_routes)