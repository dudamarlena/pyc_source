# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_with_jac.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Example for demonstrating the use of a user supplied Jacobian
    
    ODE:
    
    .. math::
       
       \dot y_1 &= y_2 \\
       \dot y_2 &= -9.82
       
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
       
    """

    def f(t, y):
        yd_0 = y[1]
        yd_1 = -9.82
        return N.array([yd_0, yd_1])

    def jac(t, y):
        j = N.array([[0, 1.0], [0, 0]])
        return j

    y0 = [
     1.0, 0.0]
    exp_mod = Explicit_Problem(f, y0, name='Example using analytic Jacobian')
    exp_mod.jac = jac
    exp_sim = CVode(exp_mod)
    exp_sim.iter = 'Newton'
    exp_sim.discr = 'BDF'
    exp_sim.atol = 1e-05
    exp_sim.rtol = 1e-05
    t, y = exp_sim.simulate(5, 1000)
    nose.tools.assert_almost_equal(y[(-1)][0], -121.75, 4)
    nose.tools.assert_almost_equal(y[(-1)][1], -49.1)
    if with_plots:
        P.plot(t, y, linestyle='dashed', marker='o')
        P.xlabel('Time')
        P.ylabel('State')
        P.title(exp_mod.name)
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()