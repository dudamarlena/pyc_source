# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_basic_backward.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    """
    The same as example :doc:`EXAMPLE_cvode_basic`  but now integrated backwards in time.
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
       
    """

    def f(t, y):
        ydot = -y[0]
        return N.array([ydot])

    exp_mod = Explicit_Problem(f, t0=5, y0=0.02695, name='CVode Test Example (reverse time): $\\dot y = - y$ ')
    exp_sim = CVode(exp_mod)
    exp_sim.iter = 'Newton'
    exp_sim.discr = 'BDF'
    exp_sim.atol = [1e-08]
    exp_sim.rtol = 1e-08
    exp_sim.backward = True
    t, y = exp_sim.simulate(0)
    nose.tools.assert_almost_equal(float(y[(-1)]), 4.0, 3)
    if with_plots:
        P.plot(t, y, color='b')
        P.title(exp_mod.name)
        P.ylabel('y')
        P.xlabel('Time')
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()