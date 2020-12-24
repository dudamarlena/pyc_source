# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_with_preconditioning.py
# Compiled at: 2017-12-28 04:09:42
"""
Example by Johannes Herold
"""
import numpy as np, nose
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Example to demonstrate the use of a preconditioner
    
    .. math::
        
        \dot y_1 & = 2 t \sin y_1  + t \sin y_2 \\
        \dot y_2 & = 3 t \sin y_1  + 2 t \sin y_2
        
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
       
    """

    def rhs(t, y):
        A = np.array([[2.0, 1.0], [3.0, 2.0]])
        yd = np.dot(A * t, np.sin(y))
        return yd

    def prec_setup(t, y, fy, jok, gamma, data):
        A = np.array([[2.0, 1.0], [3.0, 2.0]])
        if jok == False:
            a0 = A[(0, 0)] * t * np.cos(y[0])
            a1 = A[(1, 1)] * t * np.cos(y[1])
            a = np.array([1.0 - gamma * a0, 1.0 - gamma * a1])
            return [
             True, a]
        if jok == True:
            return [
             False, data]

    def prec_solve(t, y, fy, r, gamma, delta, data):
        z0 = r[0] / data[0]
        z1 = r[1] / data[1]
        z = np.array([z0, z1])
        return z

    y0 = [
     1.0, 2.0]
    exp_mod = Explicit_Problem(rhs, y0, name='Example of using a preconditioner in SUNDIALS')
    exp_mod.prec_setup = prec_setup
    exp_mod.prec_solve = prec_solve
    exp_sim = CVode(exp_mod)
    exp_sim.iter = 'Newton'
    exp_sim.discr = 'BDF'
    exp_sim.atol = 1e-05
    exp_sim.rtol = 1e-05
    exp_sim.linear_solver = 'SPGMR'
    exp_sim.precond = 'PREC_RIGHT'
    t, y = exp_sim.simulate(5)
    nose.tools.assert_almost_equal(y[(-1, 0)], 3.11178295, 4)
    nose.tools.assert_almost_equal(y[(-1, 1)], 3.19318992, 4)
    if with_plots:
        exp_sim.plot()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()