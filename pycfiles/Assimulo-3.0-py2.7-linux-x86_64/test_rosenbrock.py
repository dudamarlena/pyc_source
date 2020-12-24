# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_rosenbrock.py
# Compiled at: 2018-10-13 05:07:25
import nose
from assimulo import testattr
from assimulo.solvers.rosenbrock import *
from assimulo.problem import Explicit_Problem
from assimulo.exception import *
import scipy.sparse as sp

class Test_RodasODE:

    def setUp(self):

        def f(t, y):
            eps = 1e-06
            my = 1.0 / eps
            yd_0 = y[1]
            yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
            return N.array([yd_0, yd_1])

        def jac(t, y):
            eps = 1e-06
            my = 1.0 / eps
            j = N.array([[0.0, 1.0], [my * (-2.0 * y[0] * y[1] - 1.0), my * (1.0 - y[0] ** 2)]])
            return j

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
        exp_mod = Explicit_Problem(f, y0, name='Van der Pol (explicit)')
        exp_mod_sp = Explicit_Problem(f, y0, name='Van der Pol (explicit)')
        exp_mod.jac = jac
        exp_mod_sp.jac = jac_sparse
        self.mod = exp_mod
        self.mod_sp = exp_mod_sp

    @testattr(stddist=True)
    def test_nbr_fcn_evals_due_to_jac(self):
        sim = RodasODE(self.mod)
        sim.usejac = False
        sim.simulate(1)
        assert sim.statistics['nfcnjacs'] > 0
        sim = RodasODE(self.mod)
        sim.simulate(1)
        assert sim.statistics['nfcnjacs'] == 0

    @testattr(stddist=True)
    def test_usejac_csc_matrix(self):
        sim = RodasODE(self.mod_sp)
        sim.usejac = True
        sim.simulate(2.0)
        assert sim.statistics['nfcnjacs'] == 0
        nose.tools.assert_almost_equal(sim.y_sol[(-1)][0], 1.706168035, 4)