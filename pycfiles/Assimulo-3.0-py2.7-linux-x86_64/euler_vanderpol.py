# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/euler_vanderpol.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import ImplicitEuler
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Example for the use of the implicit Euler method to solve
    Van der Pol's equation
    
    .. math::
       
        \dot y_1 &= y_2 \\
        \dot y_2 &= \mu ((1.-y_1^2) y_2-y_1)

    with :math:`\mu=\frac{1}{5} 10^3`.

    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance

    """
    eps = 0.005
    my = 1.0 / eps

    def f(t, y):
        yd_0 = y[1]
        yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
        return N.array([yd_0, yd_1])

    def jac(t, y):
        jd_00 = 0.0
        jd_01 = 1.0
        jd_10 = -1.0 * my - 2 * y[0] * y[1] * my
        jd_11 = my * (1.0 - y[0] ** 2)
        return N.array([[jd_00, jd_01], [jd_10, jd_11]])

    y0 = [
     2.0, -0.6]
    exp_mod = Explicit_Problem(f, y0, name="ImplicitEuler: Van der Pol's equation (as explicit problem) ")
    exp_mod.jac = jac
    exp_sim = ImplicitEuler(exp_mod)
    exp_sim.h = 0.0001
    exp_sim.usejac = True
    t, y = exp_sim.simulate(2.0)
    if with_plots:
        P.plot(t, y[:, 0], marker='o')
        P.title(exp_mod.name)
        P.ylabel('State: $y_1$')
        P.xlabel('Time')
        P.show()
    x1 = y[:, 0]
    assert N.abs(x1[(-1)] - 1.8601438) < 0.1
    return (
     exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()