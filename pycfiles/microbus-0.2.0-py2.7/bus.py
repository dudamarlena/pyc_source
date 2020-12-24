# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/bus.py
# Compiled at: 2018-01-30 16:37:48
import logging
logger = logging.getLogger(__name__)

class SimultaneousRoutesException(Exception):
    pass


class Bus(object):

    def __init__(self, keep_prev=0):
        super(Bus, self).__init__()
        self._prev_routes = [None] * keep_prev
        self.current_route = None
        self._completed_routes = 0
        return

    @property
    def prev_routes(self):
        return self._prev_routes

    @property
    def completed_routes(self):
        return self._completed_routes

    def depart(self, route):
        if self.current_route is not None:
            raise SimultaneousRoutesException("Can't depart 2 routes using same bus")
        else:
            self.add_to_history(route)
            return self._depart(route)
        return

    def add_to_history(self, route):
        if len(self.prev_routes):
            self._prev_routes.pop()
            self._prev_routes.insert(0, route)

    def _depart(self, route):
        if self.current_route is not None:
            raise SimultaneousRoutesException()
        self.current_route = route
        onboard = []
        try:
            while len(self.current_route):
                stop = self.current_route[0]
                curr_stop = stop
                self.unboard(onboard, curr_stop)
                onboard = []
                if stop is not self.current_route[(-1)]:
                    onboard = self.board(curr_stop)
                self.current_route = self.current_route[1:]
                yield (stop, self.current_route)

        finally:
            if not len(self.current_route):
                self._completed_routes += 1
            self.current_route = None

        return

    def board(self, stop):
        passengers = []
        for p in stop:
            passengers.append(p)

        return passengers

    def unboard(self, passengers, stop):
        if len(passengers):
            stop.arrive(passengers)