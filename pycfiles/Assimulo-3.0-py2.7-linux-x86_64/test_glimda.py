# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_glimda.py
# Compiled at: 2017-12-28 04:09:42
import nose
from assimulo import testattr
from assimulo.solvers import GLIMDA
from assimulo.problem import Implicit_Problem, Explicit_Problem
from assimulo.exception import *
import numpy as N

class Test_GLIMDA:
    """
    Tests the GLIMDA solver.
    """

    def setUp(self):
        """
        This sets up the test case.
        """

        def f(t, y, yd):
            eps = 1e-06
            my = 1.0 / eps
            yd_0 = y[1]
            yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
            res_0 = yd[0] - yd_0
            res_1 = yd[1] - yd_1
            return N.array([res_0, res_1])

        y0 = [
         2.0, -0.6]
        yd0 = [-0.6, -200000.0]
        self.mod = Implicit_Problem(f, y0, yd0)
        self.mod_t0 = Implicit_Problem(f, y0, yd0, 1.0)
        self.sim = GLIMDA(self.mod)
        self.sim_t0 = GLIMDA(self.mod_t0)
        self.sim.atol = 0.0001
        self.sim.rtol = 0.0001
        self.sim.inith = 0.0001

    @testattr(stddist=True)
    def test_simulate_explicit(self):
        """
        Test a simulation of an explicit problem using GLIMDA.
        """
        f = lambda t, y: N.array(-y)
        y0 = [1.0]
        problem = Explicit_Problem(f, y0)
        simulator = GLIMDA(problem)
        assert simulator.yd0[0] == -simulator.y0[0]
        t, y = simulator.simulate(1.0)
        nose.tools.assert_almost_equal(float(y[(-1)]), float(N.exp(-1.0)), 4)

    @testattr(stddist=True)
    def test_maxord(self):
        """
        Tests the maximum order of GLIMDA.
        """
        assert self.sim.maxord == 3
        assert self.sim.options['maxord'] == 3
        self.sim.maxord = 2
        assert self.sim.maxord == 2
        assert self.sim.options['maxord'] == 2
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_maxord, 4)
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_maxord, 0)

    @testattr(stddist=True)
    def test_minord(self):
        """
        Tests the minimum order of GLIMDA.
        """
        assert self.sim.minord == 1
        assert self.sim.options['minord'] == 1
        self.sim.minord = 2
        assert self.sim.minord == 2
        assert self.sim.options['minord'] == 2
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_minord, 4)
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_minord, 0)

    @testattr(stddist=True)
    def test_maxsteps(self):
        """
        Tests the maximum allowed steps of GLIMDA
        """
        assert self.sim.maxsteps == 100000
        assert self.sim.options['maxsteps'] == 100000
        self.sim.maxsteps = 100
        assert self.sim.maxsteps == 100
        assert self.sim.options['maxsteps'] == 100
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_maxsteps, -1)

    @testattr(stddist=True)
    def test_newt(self):
        """
        Tests the maximum allowed number of Newton iterations GLIMDA
        """
        assert self.sim.newt == 5
        assert self.sim.options['newt'] == 5
        self.sim.newt = 3
        assert self.sim.newt == 3
        assert self.sim.options['newt'] == 3
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_newt, -1)

    @testattr(stddist=True)
    def test_minh(self):
        """
        Tests the minimum stepsize of GLIMDA.
        """
        assert self.sim.minh == N.finfo(N.double).eps
        assert self.sim.options['minh'] == N.finfo(N.double).eps
        self.sim.minh = 1e-05
        assert self.sim.minh == 1e-05
        assert self.sim.options['minh'] == 1e-05

    @testattr(stddist=True)
    def test_order(self):
        """
        Tests the order of GLIMDA.
        """
        assert self.sim.order == 0
        assert self.sim.options['order'] == 0
        self.sim.order = 1
        assert self.sim.order == 1
        assert self.sim.options['order'] == 1
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_order, -1)

    @testattr(stddist=True)
    def test_maxh(self):
        """
        Tests the maximum stepsize of GLIMDA.
        """
        assert self.sim.maxh == N.inf
        assert self.sim.options['maxh'] == N.inf
        self.sim.maxh = 100000.0
        assert self.sim.maxh == 100000.0
        assert self.sim.options['maxh'] == 100000.0

    @testattr(stddist=True)
    def test_maxretry(self):
        """
        Tests the maximum number of retries of GLIMDA.
        """
        assert self.sim.maxretry == 15
        assert self.sim.options['maxretry'] == 15
        self.sim.maxretry = 10
        assert self.sim.maxretry == 10
        assert self.sim.options['maxretry'] == 10
        nose.tools.assert_raises(GLIMDA_Exception, self.sim._set_maxretry, -1)