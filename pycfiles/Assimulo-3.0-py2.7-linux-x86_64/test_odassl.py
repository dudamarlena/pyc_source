# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_odassl.py
# Compiled at: 2017-12-28 04:09:42
import nose
from assimulo import testattr
from assimulo.solvers.odassl import *
from assimulo.problem import Explicit_Problem
from assimulo.problem import Implicit_Problem
from assimulo.problem import Overdetermined_Problem
from assimulo.exception import *
import numpy as np

class Test_ODASSL:

    def setUp(self):
        """
        This function sets up the test case.
        """
        f = lambda t, y, yd: yd + 1
        y0 = [1.0, 1.0, 1.0]
        yd0 = [-1.0, -1.0, -1.0]
        self.problem = Overdetermined_Problem(f, y0, yd0)
        self.simulator = ODASSL(self.problem)

    @testattr(stddist=True)
    def test_overdetermined(self):
        f = lambda t, y, yd: np.hstack((yd + 1, yd + 1))
        y0 = [1.0, 1.0, 1.0]
        yd0 = [-1.0, -1.0, -1.0]
        self.problem = Overdetermined_Problem(f, y0, yd0)
        self.simulator = ODASSL(self.problem)
        self.simulator.simulate(1)

    @testattr(stddist=True)
    def test_implicit_problem(self):
        f = lambda t, y, yd: yd + 1
        y0 = [1.0, 1.0, 1.0]
        yd0 = [-1.0, -1.0, -1.0]
        self.problem = Implicit_Problem(f, y0, yd0)
        self.simulator = ODASSL(self.problem)
        self.simulator.simulate(1)

    @testattr(stddist=True)
    def test_atol(self):
        self.simulator.simulate(1)
        self.simulator.reset()
        self.simulator.atol = 1e-06
        self.simulator.simulate(1)
        self.problem.algvar = [
         1, 1, 0]
        simulator = ODASSL(self.problem)
        simulator.atol = 1e-06
        self.simulator.simulate(1)

    @testattr(stddist=True)
    def test_rtol(self):
        self.simulator.simulate(1)
        self.simulator.reset()
        self.simulator.rtol = 1e-06
        self.simulator.simulate(1)
        self.problem.algvar = [
         1, 1, 0]
        simulator = ODASSL(self.problem)
        simulator.rtol = 1e-06
        self.simulator.simulate(1)