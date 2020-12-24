# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/euler_with_disc.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import ExplicitEuler
from assimulo.problem import Explicit_Problem

class Extended_Problem(Explicit_Problem):
    y0 = [
     0.0, -1.0, 0.0]
    sw0 = [False, True, True]

    def rhs(self, t, y, sw):
        """
        This is our function we are trying to simulate. During simulation
        the parameter sw should be fixed so that our function is continuous
        over the interval. The parameters sw should only be changed when the
        integrator has stopped.
        """
        yd_0 = 1.0 if sw[0] else -1.0
        yd_1 = 0.0
        yd_2 = 0.0
        return N.array([yd_0, yd_1, yd_2])

    name = 'ODE with discontinuities and a function with consistency problem'

    def state_events(self, t, y, sw):
        """
        This is our function that keeps track of our events. When the sign
        of any of the events has changed, we have an event.
        """
        event_0 = y[1] - 1.0
        event_1 = -y[2] + 1.0
        event_2 = -t + 1.0
        return N.array([event_0, event_1, event_2])

    def handle_event(self, solver, event_info):
        """
        Event handling. This functions is called when Assimulo finds an event as
        specified by the event functions.
        """
        event_info = event_info[0]
        while True:
            self.event_switch(solver, event_info)
            b_mode = self.state_events(solver.t, solver.y, solver.sw)
            self.init_mode(solver)
            a_mode = self.state_events(solver.t, solver.y, solver.sw)
            event_info = self.check_eIter(b_mode, a_mode)
            if True not in event_info:
                break

    def event_switch(self, solver, event_info):
        """
        Turns the switches.
        """
        for i in range(len(event_info)):
            if event_info[i] != 0:
                solver.sw[i] = not solver.sw[i]

    def check_eIter(self, before, after):
        """
        Helper function for handle_event to determine if we have event
        iteration.
        
            Input: Values of the event indicator functions (state_events)
            before and after we have changed mode of operations.
        """
        eIter = [
         False] * len(before)
        for i in range(len(before)):
            if before[i] < 0.0 and after[i] > 0.0 or before[i] > 0.0 and after[i] < 0.0:
                eIter[i] = True

        return eIter

    def init_mode(self, solver):
        """
        Initialize the DAE with the new conditions.
        """
        solver.y[1] = -1.0 if solver.sw[1] else 3.0
        solver.y[2] = 0.0 if solver.sw[2] else 2.0


def run_example(with_plots=True):
    """
    Example of the use of Euler's method for a differential equation
    with a discontinuity (state event) and the need for an event iteration.
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
    """
    exp_mod = Extended_Problem()
    exp_sim = ExplicitEuler(exp_mod)
    exp_sim.verbosity = 0
    exp_sim.report_continuously = True
    t, y = exp_sim.simulate(10.0, 1000)
    nose.tools.assert_almost_equal(y[(-1)][0], 8.0)
    nose.tools.assert_almost_equal(y[(-1)][1], 3.0)
    nose.tools.assert_almost_equal(y[(-1)][2], 2.0)
    if with_plots:
        P.plot(t, y)
        P.title('Solution of a differential equation with discontinuities')
        P.ylabel('States')
        P.xlabel('Time')
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()