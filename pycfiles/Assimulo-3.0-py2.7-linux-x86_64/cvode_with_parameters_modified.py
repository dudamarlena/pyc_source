# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_with_parameters_modified.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    This is the same example from the Sundials package (cvsRoberts_FSA_dns.c)

    This simple example problem for CVode, due to Robertson, 
    is from chemical kinetics, and consists of the following three 
    equations:

    .. math:: 
    
       \dot y_1 &= -p_1 y_1 + p_2 y_2 y_3 \
       \dot y_2 &= p_1 y_1 - p_2 y_2 y_3 - p_3 y_2^2 \
       \dot y_3 &= p_3  y_2^2
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
    """

    def f(t, y, p):
        p3 = 30000000.0
        yd_0 = -p[0] * y[0] + p[1] * y[1] * y[2]
        yd_1 = p[0] * y[0] - p[1] * y[1] * y[2] - p3 * y[1] ** 2
        yd_2 = p3 * y[1] ** 2
        return N.array([yd_0, yd_1, yd_2])

    y0 = [
     1.0, 0.0, 0.0]
    exp_mod = Explicit_Problem(f, y0, name='Sundials test example: Chemical kinetics')
    exp_mod.p0 = [
     0.04, 10000.0]
    exp_mod.pbar = [0.04, 10000.0]
    exp_sim = CVode(exp_mod)
    exp_sim.iter = 'Newton'
    exp_sim.discr = 'BDF'
    exp_sim.rtol = 0.0001
    exp_sim.atol = N.array([1e-08, 1e-14, 1e-06])
    exp_sim.sensmethod = 'SIMULTANEOUS'
    exp_sim.suppress_sens = False
    exp_sim.report_continuously = True
    t, y = exp_sim.simulate(4, 400)
    nose.tools.assert_almost_equal(y[(-1)][0], 0.905518032, 4)
    nose.tools.assert_almost_equal(y[(-1)][1], 2.24046805e-05, 4)
    nose.tools.assert_almost_equal(y[(-1)][2], 0.0944595637, 4)
    nose.tools.assert_almost_equal(exp_sim.p_sol[0][(-1)][0], -1.8761, 2)
    nose.tools.assert_almost_equal(exp_sim.p_sol[1][(-1)][0], 2.9614e-06, 8)
    if with_plots:
        P.plot(t, y)
        P.xlabel('Time')
        P.ylabel('State')
        P.title(exp_mod.name)
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()