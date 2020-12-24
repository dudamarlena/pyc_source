# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/euler_basic.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import ExplicitEuler
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Demonstration of the use of the use of the explicit euler method by solving the
    linear test equation :math:`\dot y = - y`
    
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
       
    """

    def f(t, y):
        ydot = -y[0]
        return N.array([ydot])

    exp_mod = Explicit_Problem(f, 4.0, name='ExplicitEuler Example: $\\dot y = - y$')
    exp_sim = ExplicitEuler(exp_mod)
    exp_sim.options['continuous_output'] = True
    t1, y1 = exp_sim.simulate(3)
    t2, y2 = exp_sim.simulate(5, 100)
    if with_plots:
        P.plot(t1, y1, color='b')
        P.plot(t2, y2, color='r')
        P.title(exp_mod.name)
        P.ylabel('y')
        P.xlabel('Time')
        P.show()
    nose.tools.assert_almost_equal(float(y2[(-1)]), 0.02628193)
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()