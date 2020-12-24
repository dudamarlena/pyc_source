# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/radau5ode_vanderpol.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import Radau5ODE
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Example for the use of the implicit Euler method to solve
    Van der Pol's equation
    
    .. math::
       
        \dot y_1 &= y_2 \\
        \dot y_2 &= \mu ((1.-y_1^2) y_2-y_1)

    with :math:`\mu= 10^6`.

    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance

    """

    def f(t, y):
        eps = 1e-06
        my = 1.0 / eps
        yd_0 = y[1]
        yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
        return N.array([yd_0, yd_1])

    y0 = [
     2.0, -0.6]
    exp_mod = Explicit_Problem(f, y0)
    exp_mod.name = 'Van der Pol (explicit)'
    exp_sim = Radau5ODE(exp_mod)
    exp_sim.atol = 0.0001
    exp_sim.rtol = 0.0001
    exp_sim.inith = 0.0001
    t, y = exp_sim.simulate(2.0)
    print y
    if with_plots:
        P.plot(t, y[:, 0])
        P.xlabel('Time')
        P.ylabel('State')
        P.title(exp_mod.name)
        P.show()
    x1 = y[:, 0]
    assert N.abs(x1[(-1)] - 1.706168035) < 0.001
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()