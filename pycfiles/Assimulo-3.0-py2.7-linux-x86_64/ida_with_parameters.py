# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/ida_with_parameters.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import IDA
from assimulo.problem import Implicit_Problem

def run_example(with_plots=True):
    r"""
    This is the same example from the Sundials package (cvsRoberts_FSA_dns.c)
    Its purpose is to demonstrate the use of parameters in the differential equation.

    This simple example problem for IDA, due to Robertson
    see http://www.dm.uniba.it/~testset/problems/rober.php, 
    is from chemical kinetics, and consists of the system:
    
    .. math:: 
    
       \dot y_1 -( -p_1 y_1 + p_2 y_2 y_3)&=0 \\
       \dot y_2 -(p_1 y_1 - p_2 y_2 y_3 - p_3 y_2^2)&=0  \\
       \dot y_3 -( p_3  y_ 2^2)&=0 
       
    
    on return:
    
       - :dfn:`imp_mod`    problem instance
    
       - :dfn:`imp_sim`    solver instance
    
    """

    def f(t, y, yd, p):
        res1 = -p[0] * y[0] + p[1] * y[1] * y[2] - yd[0]
        res2 = p[0] * y[0] - p[1] * y[1] * y[2] - p[2] * y[1] ** 2 - yd[1]
        res3 = y[0] + y[1] + y[2] - 1
        return N.array([res1, res2, res3])

    y0 = [
     1.0, 0.0, 0.0]
    yd0 = [0.1, 0.0, 0.0]
    p0 = [0.04, 10000.0, 30000000.0]
    imp_mod = Implicit_Problem(f, y0, yd0, p0=p0)
    imp_sim = IDA(imp_mod)
    imp_sim.atol = N.array([1e-08, 1e-14, 1e-06])
    imp_sim.algvar = [1.0, 1.0, 0.0]
    imp_sim.suppress_alg = False
    imp_sim.report_continuously = True
    imp_sim.pbar = p0
    imp_sim.suppress_sens = False
    imp_sim.make_consistent('IDA_YA_YDP_INIT')
    t, y, yd = imp_sim.simulate(4, 400)
    print (imp_sim.p_sol[0][(-1)], imp_sim.p_sol[1][(-1)], imp_sim.p_sol[0][(-1)])
    nose.tools.assert_almost_equal(y[(-1)][0], 0.905518032, 4)
    nose.tools.assert_almost_equal(y[(-1)][1], 2.24046805e-05, 4)
    nose.tools.assert_almost_equal(y[(-1)][2], 0.0944595637, 4)
    nose.tools.assert_almost_equal(imp_sim.p_sol[0][(-1)][0], -1.8761, 2)
    nose.tools.assert_almost_equal(imp_sim.p_sol[1][(-1)][0], 2.9614e-06, 8)
    nose.tools.assert_almost_equal(imp_sim.p_sol[2][(-1)][0], -4.9334e-10, 12)
    if with_plots:
        P.plot(t, y)
        P.title(imp_mod.name)
        P.xlabel('Time')
        P.ylabel('State')
        P.show()
    return (imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()