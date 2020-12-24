# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/radau5dae_vanderpol.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import Radau5DAE
from assimulo.problem import Implicit_Problem

def run_example(with_plots=True):
    r"""
    Example for the use of Radau5DAE to solve
    Van der Pol's equation
    
    .. math::
       
        \dot y_1 &= y_2 \\
        \dot y_2 &= \mu ((1.-y_1^2) y_2-y_1)

    with :math:`\mu= 10^6`.

    on return:
    
       - :dfn:`imp_mod`    problem instance
    
       - :dfn:`imp_sim`    solver instance

    """

    def f(t, y, yd):
        eps = 1e-06
        my = 1.0 / eps
        yd_0 = y[1]
        yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
        res_0 = yd[0] - yd_0
        res_1 = yd[1] - yd_1
        return N.array([res_0, res_1])

    y0 = [
     2.0, -0.6]
    yd0 = [-0.6, -200000.0]
    imp_mod = Implicit_Problem(f, y0, yd0)
    imp_mod.name = 'Van der Pol (implicit)'
    imp_sim = Radau5DAE(imp_mod)
    imp_sim.atol = 0.0001
    imp_sim.rtol = 0.0001
    imp_sim.inith = 0.0001
    t, y, yd = imp_sim.simulate(2.0)
    if with_plots:
        P.subplot(211)
        P.plot(t, y[:, 0])
        P.xlabel('Time')
        P.ylabel('State')
        P.subplot(212)
        P.plot(t, yd[:, 0] * 1e-05)
        P.xlabel('Time')
        P.ylabel('State derivatives scaled with $10^{-5}$')
        P.suptitle(imp_mod.name)
        P.show()
    x1 = y[:, 0]
    assert N.abs(x1[(-1)] - 1.706168035) < 0.001
    return (imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()