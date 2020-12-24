# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_odepack.py
# Compiled at: 2018-10-13 05:07:25
import nose, numpy.testing
from assimulo import testattr
from assimulo.lib.odepack import dsrcar, dcfode
from assimulo.solvers import LSODAR, odepack
from assimulo.problem import Explicit_Problem
from assimulo.exception import *
import numpy as N, scipy.sparse as sp

class Test_LSODAR:
    """
    Tests the LSODAR solver.
    """

    def setUp(self):
        """
        This sets up the test case.
        """

        def f(t, y):
            eps = 1e-06
            my = 1.0 / eps
            yd_0 = y[1]
            yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
            return N.array([yd_0, yd_1])

        def jac(t, y):
            eps = 1e-06
            my = 1.0 / eps
            J = N.zeros([2, 2])
            J[(0, 0)] = 0.0
            J[(0, 1)] = 1.0
            J[(1, 0)] = my * (-2.0 * y[0] * y[1] - 1.0)
            J[(1, 1)] = my * (1.0 - y[0] ** 2)
            return J

        def jac_sparse(t, y):
            eps = 1e-06
            my = 1.0 / eps
            J = N.zeros([2, 2])
            J[(0, 0)] = 0.0
            J[(0, 1)] = 1.0
            J[(1, 0)] = my * (-2.0 * y[0] * y[1] - 1.0)
            J[(1, 1)] = my * (1.0 - y[0] ** 2)
            return sp.csc_matrix(J)

        y0 = [
         2.0, -0.6]
        exp_mod = Explicit_Problem(f, y0)
        exp_mod_t0 = Explicit_Problem(f, y0, 1.0)
        exp_mod_sp = Explicit_Problem(f, y0)
        exp_mod.jac = jac
        exp_mod_sp.jac = jac_sparse
        self.mod = exp_mod
        self.sim = LSODAR(exp_mod)
        self.sim_sp = LSODAR(exp_mod_sp)
        self.sim.atol = 1e-06
        self.sim.rtol = 1e-06
        self.sim.usejac = False

    @testattr(stddist=True)
    def test_simulation(self):
        """
        This tests the LSODAR with a simulation of the van der pol problem.
        """
        self.sim.simulate(1.0)
        nose.tools.assert_almost_equal(self.sim.y_sol[(-1)][0], -1.863646028, 4)

    @testattr(stddist=True)
    def test_setcoefficients(self):
        elco, tesco = dcfode(1)
        nose.tools.assert_almost_equal(elco[(0, 2)], 5.0 / 12.0, 9)
        nose.tools.assert_almost_equal(tesco[(0, 2)], 2.0, 9)

    @testattr(stddist=True)
    def test_readcommon(self):
        """
        This tests the LSODAR's subroutine dsrcar  (read functionality).
        """
        self.sim.simulate(1.0)
        r = N.ones((245, ), 'd')
        i = N.ones((55, ), 'i')
        dsrcar(r, i, 1)
        nose.tools.assert_almost_equal(r[217], 2.22044605e-16, 20)
        nose.tools.assert_equal(i[36], 3)

    @testattr(stddist=True)
    def test_writereadcommon(self):
        """
        This tests the LSODAR's subroutine dsrcar  (write and read functionality).
        """
        r = N.ones((245, ), 'd')
        i = N.ones((55, ), 'i')
        dsrcar(r, i, 2)
        r[0] = 100.0
        i[0] = 10
        dsrcar(r, i, 1)
        nose.tools.assert_almost_equal(r[0], 1.0, 4)
        nose.tools.assert_equal(i[0], 1)

    def test_rkstarter(self):
        """
        This test checks the correctness of the Nordsieck array generated 
        from a RK starter
        """
        pass

    @testattr(stddist=True)
    def test_interpol(self):
        self.sim.report_continuously = True
        t_sol, y_sol = self.sim.simulate(1.0, ncp_list=[0.5])
        self.sim.reset()
        t_sol1, y_sol1 = self.sim.simulate(0.5)
        ind05 = N.nonzero(N.array(t_sol) == 0.5)[0][0]
        nose.tools.assert_almost_equal(y_sol[(ind05, 0)], y_sol1[(-1, 0)], 6)

    def test_simulation_with_jac(self):
        """
        This tests the LSODAR with a simulation of the van der pol problem.
        """
        self.sim.usejac = True
        self.sim.simulate(1.0)
        nose.tools.assert_almost_equal(self.sim.y_sol[(-1)][0], -1.863646028, 4)

    @testattr(stddist=True)
    def test_simulation_ncp(self):
        self.sim.simulate(1.0, 100)
        nose.tools.assert_almost_equal(self.sim.y_sol[(-1)][0], -1.863646028, 4)

    @testattr(stddist=True)
    def test_usejac_csc_matrix(self):
        self.sim_sp.usejac = True
        self.sim_sp.simulate(2.0)
        assert self.sim_sp.statistics['nfcnjacs'] == 0
        nose.tools.assert_almost_equal(self.sim_sp.y_sol[(-1)][0], 1.706168035, 4)

    @testattr(stddist=True)
    def test_simulation_ncp_list(self):
        self.sim.simulate(1.0, ncp_list=[0.5])
        nose.tools.assert_almost_equal(self.sim.y_sol[(-1)][0], -1.863646028, 4)

    @testattr(stddist=True)
    def test_maxh(self):
        self.sim.hmax = 1.0
        assert self.sim.options['maxh'] == 1.0
        assert self.sim.maxh == 1.0
        self.sim.maxh = 2.0
        assert self.sim.options['maxh'] == 2.0
        assert self.sim.maxh == 2.0

    @testattr(stddist=True)
    def test_simulation_ncp_list_2(self):
        self.sim.simulate(1.0, ncp_list=[0.5, 4])
        nose.tools.assert_almost_equal(self.sim.y_sol[(-1)][0], -1.863646028, 4)

    @testattr(stddist=True)
    def test_simulation_ncp_with_jac(self):
        """
        Test a simulation with ncp.
        """
        self.sim.usejac = True
        self.sim.simulate(1.0, 100)
        nose.tools.assert_almost_equal(self.sim.y_sol[(-1)][0], -1.863646028, 4)