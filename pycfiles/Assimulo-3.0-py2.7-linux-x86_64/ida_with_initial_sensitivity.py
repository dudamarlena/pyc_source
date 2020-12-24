# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/ida_with_initial_sensitivity.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import IDA
from assimulo.problem import Implicit_Problem

def run_example(with_plots=True):
    """
    This example show how to use Assimulo and IDA for simulating sensitivities
    for initial conditions.::
    
        0 = dy1/dt - -(k01+k21+k31)*y1 - k12*y2 - k13*y3 - b1
        0 = dy2/dt - k21*y1 + (k02+k12)*y2
        0 = dy3/dt - k31*y1 + k13*y3
     
        y1(0) = p1, y2(0) = p2, y3(0) = p3
        p1=p2=p3 = 0 
    
    See http://sundials.2283335.n4.nabble.com/Forward-sensitivities-for-initial-conditions-td3239724.html
    
    on return:
    
       - :dfn:`imp_mod`    problem instance
    
       - :dfn:`imp_sim`    solver instance
    
    """

    def f(t, y, yd, p):
        y1, y2, y3 = y
        yd1, yd2, yd3 = yd
        k01 = 0.0211
        k02 = 0.0162
        k21 = 0.0111
        k12 = 0.0124
        k31 = 0.0039
        k13 = 3.5e-05
        b1 = 49.3
        res_0 = -yd1 - (k01 + k21 + k31) * y1 + k12 * y2 + k13 * y3 + b1
        res_1 = -yd2 + k21 * y1 - (k02 + k12) * y2
        res_2 = -yd3 + k31 * y1 - k13 * y3
        return N.array([res_0, res_1, res_2])

    y0 = [
     0.0, 0.0, 0.0]
    yd0 = [49.3, 0.0, 0.0]
    p0 = [0.0, 0.0, 0.0]
    yS0 = N.array([[1, 0, 0], [0, 1, 0], [0, 0, 1.0]])
    imp_mod = Implicit_Problem(f, y0, yd0, p0=p0, name='Example: Computing Sensitivities')
    imp_mod.yS0 = yS0
    imp_sim = IDA(imp_mod)
    imp_sim.rtol = 1e-07
    imp_sim.atol = 1e-06
    imp_sim.pbar = [1, 1, 1]
    imp_sim.report_continuously = True
    imp_sim.sensmethod = 'SIMULTANEOUS'
    imp_sim.suppress_sens = False
    t, y, yd = imp_sim.simulate(400)
    nose.tools.assert_almost_equal(y[(-1)][0], 1577.6552477, 3)
    nose.tools.assert_almost_equal(y[(-1)][1], 611.9574565, 3)
    nose.tools.assert_almost_equal(y[(-1)][2], 2215.88563217, 3)
    nose.tools.assert_almost_equal(imp_sim.p_sol[0][1][0], 1.0)
    if with_plots:
        P.figure(1)
        P.subplot(221)
        P.plot(t, N.array(imp_sim.p_sol[0])[:, 0], t, N.array(imp_sim.p_sol[0])[:, 1], t, N.array(imp_sim.p_sol[0])[:, 2])
        P.title('Parameter p1')
        P.legend(('p1/dy1', 'p1/dy2', 'p1/dy3'))
        P.subplot(222)
        P.plot(t, N.array(imp_sim.p_sol[1])[:, 0], t, N.array(imp_sim.p_sol[1])[:, 1], t, N.array(imp_sim.p_sol[1])[:, 2])
        P.title('Parameter p2')
        P.legend(('p2/dy1', 'p2/dy2', 'p2/dy3'))
        P.subplot(223)
        P.plot(t, N.array(imp_sim.p_sol[2])[:, 0], t, N.array(imp_sim.p_sol[2])[:, 1], t, N.array(imp_sim.p_sol[2])[:, 2])
        P.title('Parameter p3')
        P.legend(('p3/dy1', 'p3/dy2', 'p3/dy3'))
        P.subplot(224)
        P.title('ODE Solution')
        P.plot(t, y)
        P.suptitle(imp_mod.name)
        P.show()
        return (
         imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()