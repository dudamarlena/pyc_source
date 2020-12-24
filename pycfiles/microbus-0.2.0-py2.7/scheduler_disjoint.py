# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microbus/scheduler_disjoint.py
# Compiled at: 2018-01-30 16:37:48
from microbus.scheduler import BusScheduler

class DisjointRoutesBusScheduler(BusScheduler):

    def __init__(self, bus):
        super(DisjointRoutesBusScheduler, self).__init__(bus)
        self.scheduledAssignments = []
        self.currentAssignment = None
        return

    def verify_route(self, route):
        if self.currentAssignment is not None and route in self.currentAssignment:
            return False
        else:
            for assignment in self.scheduledAssignments:
                if route in assignment.route:
                    return False

            return True

    def schedule_assignment(self, assignment):
        if self.verify_route(assignment.route):
            self.scheduledAssignments.append(assignment)
            super(DisjointRoutesBusScheduler, self).schedule_assignment(lambda : self.execute_assignment(assignment))

    def execute_assignment(self, assignment):
        self.currentAssignment = assignment
        self.remove_scheduled_assignment(assignment)
        assignment()
        self.currentAssignment = None
        return

    def remove_scheduled_assignment(self, assignment):
        self.scheduledAssignments.pop(self.scheduledAssignments.index(assignment))