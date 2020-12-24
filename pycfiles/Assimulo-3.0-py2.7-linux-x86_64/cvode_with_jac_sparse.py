# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_with_jac_sparse.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, scipy.sparse as SP, pylab as P, nose
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Example for demonstrating the use of a user supplied Jacobian (sparse).
    Note that this will only work if Assimulo has been configured with
    Sundials + SuperLU. Based on the SUNDIALS example cvRoberts_sps.c
    
    ODE:
    
    .. math::
       
       \dot y_1 &= -0.04y_1 + 1e4 y_2 y_3 \\
       \dot y_2 &= - \dot y_1 - \dot y_3 \\
       \dot y_3 &= 3e7 y_2^2
       
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
       
    """

    def f(t, y):
        yd_0 = -0.04 * y[0] + 10000.0 * y[1] * y[2]
        yd_2 = 30000000.0 * y[1] * y[1]
        yd_1 = -yd_0 - yd_2
        return N.array([yd_0, yd_1, yd_2])

    def jac(t, y):
        colptrs = [
         0, 3, 6, 9]
        rowvals = [0, 1, 2, 0, 1, 2, 0, 1, 2]
        data = [-0.04, 0.04, 0.0, 10000.0 * y[2], -10000.0 * y[2] - 60000000.0 * y[1], 60000000.0 * y[1], 10000.0 * y[1], -10000.0 * y[1], 0.0]
        J = SP.csc_matrix((data, rowvals, colptrs))
        return J

    y0 = [
     1.0, 0.0, 0.0]
    exp_mod = Explicit_Problem(f, y0, name='Example using analytic (sparse) Jacobian')
    exp_mod.jac = jac
    exp_mod.jac_nnz = 9
    exp_sim = CVode(exp_mod)
    exp_sim.iter = 'Newton'
    exp_sim.discr = 'BDF'
    exp_sim.atol = [1e-08, 1e-14, 1e-06]
    exp_sim.rtol = 0.0001
    exp_sim.linear_solver = 'sparse'
    t, y = exp_sim.simulate(0.4)
    nose.tools.assert_almost_equal(y[(-1)][0], 0.9851, 3)
    if with_plots:
        P.plot(t, y[:, 1], linestyle='dashed', marker='o')
        P.xlabel('Time')
        P.ylabel('State')
        P.title(exp_mod.name)
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()