# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/assignment.py
# Compiled at: 2018-01-30 16:37:48
import microbus
from microbus.bus import Bus

class BusAssignment(object):

    def __init__(self, bus, route):
        self.bus = bus
        self.route = route
        self._finished = False

    @property
    def finished(self):
        return self._finished

    def __contains__(self, item):
        if isinstance(item, Bus):
            return self.bus == item
        else:
            if isinstance(item, microbus.BusRoute) or isinstance(item, microbus.BusStop):
                if self.finished:
                    return False
                if self.bus.current_route is None:
                    return item in self.route
                return item in self.bus.current_route
            return False

    def __call__(self, *args, **kwargs):
        for _ in self.bus.depart(self.route):
            pass

        self._finished = True