# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/scheduler.py
# Compiled at: 2018-01-30 16:37:48
from zyklus import Zyklus
from microbus import BusRoute
from microbus.assignment import BusAssignment

class BusScheduler(object):

    def __init__(self, bus):
        self.bus = bus
        self.zyklus = Zyklus()

    def schedule(self, route):
        assert type(route) is BusRoute
        self.schedule_assignment(BusAssignment(self.bus, route))

    def schedule_assignment(self, assignment):
        self.zyklus.post(assignment)

    def run(self):
        self.zyklus.loop()

    def end(self):
        self.zyklus.terminate()