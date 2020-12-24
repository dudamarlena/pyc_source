# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/stop.py
# Compiled at: 2018-01-30 16:37:48


class BusStop(object):

    def __init__(self, name='', arriving_passengers_handler=None, waiting_passengers_callback=None):
        self.name = name
        self.departuringData = []
        self.arrivingPassengersHandler = arriving_passengers_handler
        self.passengersWaitingCallback = waiting_passengers_callback

    def id(self):
        return str(id(self))

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.departuringData)

    def wait_for_bus(self, data):
        self.departuringData.append(data)
        if len(self.departuringData) == 1 and self.passengersWaitingCallback is not None:
            self.passengersWaitingCallback(self)
        return

    def __iter__(self):
        while len(self.departuringData):
            yield self.departuringData.pop(0)

    def arrive(self, passengers):
        if self.arrivingPassengersHandler is not None:
            self.arrivingPassengersHandler(self, passengers)
        return