# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/test_solvers.py
# Compiled at: 2017-12-28 04:09:42
import nose, numpy as np
from assimulo import testattr
from assimulo.exception import *
from assimulo.problem import *
from assimulo.solvers import Radau5DAE, Radau5ODE, Dopri5, RodasODE

def res(t, y, yd, sw):
    return np.array([yd + y])


def state_events(t, y, yd, sw):
    return y - 0.5


def rhs(t, y, sw):
    return np.array([-y])


def estate_events(t, y, sw):
    return y - 0.5


problem = Implicit_Problem(res, [1.0], [-1.0])
problem.state_events = state_events
eproblem = Explicit_Problem(rhs, [1.0])
eproblem.state_events = estate_events

class Test_Solvers:

    @testattr(stddist=True)
    def test_radau5dae_state_events(self):
        solver = Radau5DAE(problem)
        t, y, yd = solver.simulate(2, 33)
        nose.tools.assert_almost_equal(float(y[(-1)]), 0.135, 3)

    @testattr(stddist=True)
    def test_radau5ode_state_events(self):
        solver = Radau5ODE(eproblem)
        t, y = solver.simulate(2, 33)
        nose.tools.assert_almost_equal(float(y[(-1)]), 0.135, 3)

    @testattr(stddist=True)
    def test_dopri5_state_events(self):
        solver = Dopri5(eproblem)
        t, y = solver.simulate(2, 33)
        nose.tools.assert_almost_equal(float(y[(-1)]), 0.135, 3)

    @testattr(stddist=True)
    def test_rodasode_state_events(self):
        solver = RodasODE(eproblem)
        t, y = solver.simulate(2, 33)
        nose.tools.assert_almost_equal(float(y[(-1)]), 0.135, 3)