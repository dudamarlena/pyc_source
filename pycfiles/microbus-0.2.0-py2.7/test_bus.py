# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/test_bus.py
# Compiled at: 2018-01-30 16:37:48
import unittest, microbus
from microbus.bus import Bus, SimultaneousRoutesException
from microbus.test_stop import CallbackFunc

class WaitForBusCallback(CallbackFunc):

    def __init__(self):
        super(WaitForBusCallback, self).__init__()
        self.stop = None
        return

    def __call__(self, *args, **kwargs):
        super(WaitForBusCallback, self).__call__(*args, **kwargs)
        for item in args[1]:
            self.stop.wait_for_bus(item)


class BusTest(unittest.TestCase):

    def setUp(self):
        self.stop1ArrivingPassengersHandler = WaitForBusCallback()
        self.stop2ArrivingPassengersHandler = WaitForBusCallback()
        self.stop3ArrivingPassengersHandler = WaitForBusCallback()
        self.stop1Passengers = [
         'a', 'b', 'c']
        self.stop2Passengers = ['d', 'e', 'f']
        self.stop3Passengers = ['g', 'h', 'i']
        self.stop1 = microbus.BusStop('stop1', self.stop1ArrivingPassengersHandler)
        self.stop1ArrivingPassengersHandler.stop = self.stop1
        self.stop2 = microbus.BusStop('stop2', self.stop2ArrivingPassengersHandler)
        self.stop2ArrivingPassengersHandler.stop = self.stop2
        self.stop3 = microbus.BusStop('stop3', self.stop3ArrivingPassengersHandler)
        self.stop3ArrivingPassengersHandler.stop = self.stop3
        self.stops = [
         self.stop1, self.stop2, self.stop3]
        list(map(lambda p: self.stop1.wait_for_bus(p), self.stop1Passengers))
        list(map(lambda p: self.stop2.wait_for_bus(p), self.stop2Passengers))
        list(map(lambda p: self.stop3.wait_for_bus(p), self.stop3Passengers))
        self.busRoute = microbus.BusRoute(self.stops, name='test')
        self.bus = Bus()

    def test_simulatenous_routes(self):
        weg = self.bus.depart(self.busRoute)
        next(weg)
        try:
            self.bus.depart(self.busRoute)
            raise AssertionError("shouldn't allow")
        except SimultaneousRoutesException:
            pass

        for _ in weg:
            pass

        weg1 = self.bus.depart(self.busRoute)
        weg2 = self.bus.depart(self.busRoute)
        weg3 = self.bus.depart(self.busRoute)
        next(weg2)
        try:
            next(weg1)
        except SimultaneousRoutesException:
            pass

        weg2.close()
        next(weg3)
        weg3.close()
        self.bus.depart(self.busRoute)

    def test_completedRoutes(self):
        self.assertEqual(0, self.bus.completed_routes)
        weg = self.bus.depart(self.busRoute)
        self.assertEqual(0, self.bus.completed_routes)
        for _ in weg:
            pass

        self.assertEqual(1, self.bus.completed_routes)
        for _ in self.bus.depart(self.busRoute):
            pass

        self.assertEqual(2, self.bus.completed_routes)
        weg = self.bus.depart(self.busRoute)
        next(weg)
        weg.close()
        self.assertEqual(2, self.bus.completed_routes)
        weg = self.bus.depart(self.busRoute)
        next(weg)
        self.assertEqual(2, self.bus.completed_routes)
        next(weg)
        self.assertEqual(2, self.bus.completed_routes)
        next(weg)
        self.assertEqual(2, self.bus.completed_routes)
        try:
            next(weg)
        except StopIteration:
            pass

        self.assertEqual(3, self.bus.completed_routes)

    def test_add_to_history(self):
        weg = self.bus.depart(self.busRoute)
        self.assertEqual(0, len(self.bus.prev_routes))
        weg.close()
        self.assertEqual(0, len(self.bus.prev_routes))
        route1 = self.busRoute
        route2 = route1[::-1]
        route3 = route2[1:]
        busmem = Bus(keep_prev=2)
        weg = busmem.depart(route1)
        weg.close()

    def test_iteration(self):
        for _, _ in self.bus.depart(self.busRoute):
            pass

        self.assertEqual(1, self.bus.completed_routes)

    def test_depart(self):
        gen = self.bus.depart(self.busRoute)
        stop, remainingRoute = next(gen)
        self.assertEqual(stop, self.stop1)
        self.assertEqual(2, len(remainingRoute))
        self.assertEqual(self.stop2, remainingRoute[0])
        self.assertEqual(self.stop3, remainingRoute[1])
        stop, remainingRoute = next(gen)
        self.assertEqual(stop, self.stop2)
        self.assertEqual(1, len(remainingRoute))
        self.assertEqual(self.stop3, remainingRoute[0])
        stop, remainingRoute = next(gen)
        self.assertEqual(stop, self.stop3)
        self.assertEqual(0, len(remainingRoute))
        try:
            next(gen)
            raise AssertionError()
        except StopIteration:
            pass

        self.assertEqual(0, len(self.stop1.departuringData))
        self.assertEqual(0, len(self.stop2.departuringData))
        self.assertEqual(0, len(self.stop1ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop2ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop3ArrivingPassengersHandler))
        self.assertEqual(self.stop1Passengers, list(self.stop2ArrivingPassengersHandler[0][1]))
        self.assertEqual(self.stop2Passengers + self.stop1Passengers, list(self.stop3ArrivingPassengersHandler[0][1]))
        self.assertEqual(self.stop3Passengers + self.stop2Passengers + self.stop1Passengers, self.stop3.departuringData)

    def test_board(self):
        passengers = self.bus.board(self.stop1)
        self.assertEqual(self.stop1Passengers, passengers)
        self.assertEqual(0, len(self.stop1))

    def test_unboard(self):
        self.bus.unboard(self.stop1Passengers[:], self.stop2)
        self.assertEqual(self.stop1Passengers, list(self.stop2ArrivingPassengersHandler[0][1]))