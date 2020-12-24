# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/dasp3_basic.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
try:
    from assimulo.solvers import DASP3ODE
except ImportError:
    pass

from assimulo.problem import SingPerturbed_Problem

def run_example(with_plots=True):
    r"""
    Example to demonstrate the use of DASP3 for a
    singularly perturbed problem:
    
    Slow part of the problem:
    
    .. math::
       
       \dot y_1 &= -(0.6 z + 0.8 y_3) y_1 + 10 y_2 \\
       \dot y_2 &= -10 y_2 + 1.6 z_1 y_3 \\
       \dot y_3 &= -1.33 \varepsilon ^2 y_3 ( y_1 + 2 z)
       
    with :math:`\varepsilon = \frac{1}{3} 10^{-3}`.
    
    Fast part of the problem:
    
    .. math::
    
       \dot z = 1.6 z y_3 - 6 z y_1 - 45 (\varepsilon z)^2 + 0.8 y_3 y_1
       
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
     
    """

    def dydt(t, y, z):
        eps = 1.0 / 3 * 0.001
        yp = N.array([-(0.6 * z[0] + 0.8 * y[2]) * y[0] + 10.0 * y[1],
         -10.0 * y[1] + 1.6 * z[0] * y[2],
         -1.33 * eps ** 2 * y[2] * (y[0] + 2.0 * z[0])])
        return yp

    def dzdt(t, y, z):
        eps = 1.0 / 3 * 0.001
        zp = N.array([
         1.6 * z[0] * y[2] - 0.6 * z[0] * y[0] - 45.0 * (eps * z[0]) ** 2 + 0.8 * y[2] * y[0]])
        return zp

    y0 = [
     3.0, 0.216, 1.0]
    z0 = [1.35]
    eps = N.array([0.00033333333])
    exp_mod = SingPerturbed_Problem(dydt, dzdt, yy0=y0, zz0=z0, eps=eps, name='DASP3 Example: Singularly perturbed ODE')
    exp_sim = DASP3ODE(exp_mod)
    exp_sim.rtol = 1e-05
    exp_sim.atol = 1e-05
    t, y = exp_sim.simulate(10)
    nose.tools.assert_almost_equal(y[(-1, 0)], 10.860063849896818, 3)
    if with_plots:
        P.semilogy(t, y, color='b')
        P.grid()
        P.title(exp_mod.name + ' $\\varepsilon = \\frac{1}{3} 10^{-3}$')
        P.xlabel('Time')
        P.ylabel('y')
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()