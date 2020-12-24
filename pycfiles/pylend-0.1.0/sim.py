# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/sim/sim.py
# Compiled at: 2015-11-16 08:17:20
__doc__ = '\nSimulation.\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'
from lems.base.base import LEMSBase
from lems.base.errors import SimError
import heapq

class Simulation(LEMSBase):
    """
    Simulation class.
    """
    debug = False

    def __init__(self):
        """
        Constructor.
        """
        self.runnables = {}
        self.run_queue = []
        self.event_queue = []

    def add_runnable(self, runnable):
        """
        Adds a runnable component to the list of runnable components in
        this simulation.

        @param runnable: A runnable component
        @type runnable: lems.sim.runnable.Runnable
        """
        if runnable.id in self.runnables:
            raise SimError(('Duplicate runnable component {0}').format(runnable.id))
        self.runnables[runnable.id] = runnable

    def init_run(self):
        self.current_time = 0
        for id in self.runnables:
            self.runnables[id].do_startup()
            heapq.heappush(self.run_queue, (0, self.runnables[id]))

    def step(self):
        current_time = self.current_time
        if self.run_queue == []:
            return False
        else:
            current_time, runnable = heapq.heappop(self.run_queue)
            time = current_time
            while time == current_time:
                next_time = current_time + runnable.single_step(runnable.time_step)
                if next_time > current_time:
                    heapq.heappush(self.run_queue, (next_time, runnable))
                if self.run_queue == []:
                    break
                time, runnable = heapq.heappop(self.run_queue)
                if time > current_time:
                    heapq.heappush(self.run_queue, (time, runnable))

            self.current_time = current_time
            if self.run_queue == []:
                return False
            return True

    def run(self):
        """
        Runs the simulation.
        """
        self.init_run()
        if self.debug:
            self.dump('AfterInit: ')
        while self.step():
            pass

    def push_state(self):
        for id in self.runnables:
            self.runnables[id].push_state()

    def pop_state(self):
        for id in self.runnables:
            self.runnables[id].pop_state()

    def enable_plasticity(self):
        for id in self.runnables:
            self.runnables[id].plastic = True

    def disable_plasticity(self):
        for id in self.runnables:
            self.runnables[id].plastic = False

    def dump_runnable(self, runnable, prefix='.'):
        r = runnable
        print ('{0}...............  {1} ({2})').format(prefix, r.id, r.component.type)
        print prefix + str(r)
        ignores = ['Display', 'Line', 'OutputColumn', 'OutputFile', 'Simulation']
        verbose = r.component.type not in ignores
        if verbose:
            if r.instance_variables:
                print ('{0}    Instance variables').format(prefix)
                for vn in r.instance_variables:
                    print ('{0}      {1} = {2}').format(prefix, vn, r.__dict__[vn])

            if r.derived_variables:
                print ('{0}    Derived variables').format(prefix)
                for vn in r.derived_variables:
                    print ('{0}      {1} = {2}').format(prefix, vn, r.__dict__[vn])

        if verbose:
            keys = list(r.__dict__.keys())
            keys.sort()
            print ('{0}    Keys for {1}').format(prefix, r.id)
            for k in keys:
                key_str = str(r.__dict__[k])
                if len(key_str) > 0 and not key_str == '[]' and not key_str == '{}':
                    print ('{0}       {1} -> {2}').format(prefix, k, key_str)

        if r.array:
            for c in r.array:
                self.dump_runnable(c, prefix + '    .')

        if r.uchildren:
            for cn in r.uchildren:
                self.dump_runnable(r.uchildren[cn], prefix + '    .')

    def dump(self, prefix=''):
        print 'Runnables:'
        for id in self.runnables:
            self.dump_runnable(self.runnables[id], prefix)


class Event:
    """
    Stores data associated with an event.
    """

    def __init__(self, from_id, to_id):
        self.from_id = from_id
        self.to_id = to_id