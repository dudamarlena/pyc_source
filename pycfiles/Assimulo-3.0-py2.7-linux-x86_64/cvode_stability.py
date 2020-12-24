# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_stability.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import CVode
from assimulo.problem import Explicit_Problem

def run_example(with_plots=True):
    r"""
    Example for the use of the stability limit detection algorithm
    in CVode.
    
    .. math::
       
        \dot y_1 &= y_2 \\
        \dot y_2 &= \mu ((1.-y_1^2) y_2-y_1) \\
        \dot y_3 &= sin(ty_2)

    with :math:`\mu=\frac{1}{5} 10^3`.

    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance

    """

    class Extended_Problem(Explicit_Problem):
        order = []

        def handle_result(self, solver, t, y):
            Explicit_Problem.handle_result(self, solver, t, y)
            self.order.append(solver.get_last_order())

    eps = 0.005
    my = 1.0 / eps

    def f(t, y):
        yd_0 = y[1]
        yd_1 = my * ((1.0 - y[0] ** 2) * y[1] - y[0])
        yd_2 = N.sin(t * y[1])
        return N.array([yd_0, yd_1, yd_2])

    y0 = [
     2.0, -0.6, 0.1]
    exp_mod = Extended_Problem(f, y0, name='CVode: Stability problem')
    exp_sim = CVode(exp_mod)
    exp_sim.stablimdet = True
    exp_sim.report_continuously = True
    t, y = exp_sim.simulate(2.0)
    if with_plots:
        P.subplot(211)
        P.plot(t, y[:, 2])
        P.ylabel('State: $y_1$')
        P.subplot(212)
        P.plot(t, exp_mod.order)
        P.ylabel('Order')
        P.suptitle(exp_mod.name)
        P.xlabel('Time')
        P.show()
    x1 = y[:, 0]
    assert N.abs(x1[(-1)] - 1.8601438) < 0.1
    return (
     exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()