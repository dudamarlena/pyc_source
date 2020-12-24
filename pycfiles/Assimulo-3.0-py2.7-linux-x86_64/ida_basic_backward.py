# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/ida_basic_backward.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import IDA
from assimulo.problem import Implicit_Problem

def run_example(with_plots=True):
    """
    The same as example :doc:`EXAMPLE_cvode_basic`  but now integrated backwards in time.
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
       
    """

    def f(t, y, yd):
        res = yd[0] + y[0]
        return N.array([res])

    imp_mod = Implicit_Problem(f, t0=5, y0=0.02695, yd0=-0.02695, name='IDA Example: $\\dot y + y = 0$ (reverse time)')
    imp_sim = IDA(imp_mod)
    imp_sim.atol = [
     1e-08]
    imp_sim.rtol = 1e-08
    imp_sim.backward = True
    t, y, yd = imp_sim.simulate(0)
    nose.tools.assert_almost_equal(float(y[(-1)]), 4.0, 3)
    if with_plots:
        P.plot(t, y, color='b')
        P.xlabel('Time')
        P.ylabel('State')
        P.title(imp_mod.name)
        P.show()
    return (imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()