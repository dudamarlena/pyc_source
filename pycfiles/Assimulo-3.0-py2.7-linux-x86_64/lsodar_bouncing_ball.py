# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/lsodar_bouncing_ball.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import LSODAR
from assimulo.problem import Explicit_Problem
import sys, os

class Extended_Problem(Explicit_Problem):
    y0 = [
     2.0, 0]
    sw0 = [True, False]
    g = -9.81

    def rhs(self, t, y, sw):
        """
        This is our function we are trying to simulate. 
        """
        yd_0 = y[1]
        yd_1 = self.g
        return N.array([yd_0, yd_1])

    name = 'Bouncing Ball Problem'

    def state_events(self, t, y, sw):
        """
        This is our function that keeps track of our events. When the sign
        of any of the events has changed, we have an event.
        """
        event_0 = y[0] if sw[0] else 5
        event_1 = y[1] if sw[1] else 5
        return N.array([event_0, event_1])

    def handle_event(self, solver, event_info):
        """
        Event handling. This functions is called when Assimulo finds an event as
        specified by the event functions.
        """
        event_info = event_info[0]
        if event_info[0] != 0:
            solver.sw[0] = False
            solver.sw[1] = True
            solver.y[1] = -0.88 * solver.y[1]
        else:
            solver.sw[0] = True
            solver.sw[1] = False

    def initialize(self, solver):
        solver.h_sol = []
        solver.nq_sol = []

    def handle_result(self, solver, t, y):
        Explicit_Problem.handle_result(self, solver, t, y)
        if solver.report_continuously:
            h, nq = solver.get_algorithm_data()
            solver.h_sol.extend([h])
            solver.nq_sol.extend([nq])


def run_example(with_plots=True):
    r"""
    Bouncing ball example to demonstrate LSODAR's 
    discontinuity handling.

    Also a way to use :program:`problem.initialize` and :program:`problem.handle_result`
    in order to provide extra information is demonstrated.

    The governing differential equation is

    .. math::

       \dot y_1 &= y_2\\
       \dot y_2 &= -9.81

    and the switching functions are

    .. math::

       \mathrm{event}_0 &= y_1 \;\;\;\text{ if } \;\;\;\mathrm{sw}_0 = 1\\
       \mathrm{event}_1 &= y_2 \;\;\;\text{ if }\;\;\; \mathrm{sw}_1 = 1

    otherwise the events are deactivated by setting the respective value to something different from 0.

    The event handling sets 

    :math:`y_1 = - 0.88 y_1` and :math:`\mathrm{sw}_1 = 1` if the first event triggers 
    and :math:`\mathrm{sw}_1 = 0`   if the second event triggers.

    """
    exp_mod = Extended_Problem()
    exp_sim = LSODAR(exp_mod)
    exp_sim.atol = 1e-08
    exp_sim.report_continuously = True
    exp_sim.verbosity = 30
    t, y = exp_sim.simulate(10.0)
    if with_plots:
        P.subplot(221)
        P.plot(t, y)
        P.title('LSODAR Bouncing ball (one step mode)')
        P.ylabel('States: $y$ and $\\dot y$')
        P.subplot(223)
        P.plot(exp_sim.t_sol, exp_sim.h_sol)
        P.title('LSODAR step size plot')
        P.xlabel('Time')
        P.ylabel('Sepsize')
        P.subplot(224)
        P.plot(exp_sim.t_sol, exp_sim.nq_sol)
        P.title('LSODAR order plot')
        P.xlabel('Time')
        P.ylabel('Order')
        P.suptitle(exp_mod.name)
        P.show()
    return (
     exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()