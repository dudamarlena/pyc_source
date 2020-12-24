# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/ida_with_user_defined_handle_result.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P
from assimulo.solvers import IDA
from assimulo.problem import Implicit_Problem
import nose

def run_example(with_plots=True):
    r"""
    Example for demonstrating the use of a user supplied Jacobian
    
    ODE:
    
    .. math::
       
        \dot y_1-y_3 &= 0 \\
        \dot y_2-y_4 &= 0 \\
        \dot y_3+y_5 y_1 &= 0 \\
        \dot y_4+y_5 y_2+9.82&= 0 \\
        y_3^2+y_4^2-y_5(y_1^2+y_2^2)-9.82 y_2&= 0 
    
    on return:
    
       - :dfn:`imp_mod`    problem instance
    
       - :dfn:`imp_sim`    solver instance
       
    """
    global order
    order = []

    def f(t, y, yd):
        res_0 = yd[0] - y[2]
        res_1 = yd[1] - y[3]
        res_2 = yd[2] + y[4] * y[0]
        res_3 = yd[3] + y[4] * y[1] + 9.82
        res_4 = y[2] ** 2 + y[3] ** 2 - y[4] * (y[0] ** 2 + y[1] ** 2) - y[1] * 9.82
        return N.array([res_0, res_1, res_2, res_3, res_4])

    def handle_result(solver, t, y, yd):
        order.append(solver.get_last_order())
        solver.t_sol.extend([t])
        solver.y_sol.extend([y])
        solver.yd_sol.extend([yd])

    y0 = [
     1.0, 0.0, 0.0, 0.0, 5]
    yd0 = [0.0, 0.0, 0.0, -9.82, 0.0]
    imp_mod = Implicit_Problem(f, y0, yd0, name='Example for plotting used order')
    imp_mod.handle_result = handle_result
    imp_mod.algvar = [
     1.0, 1.0, 1.0, 1.0, 0.0]
    imp_sim = IDA(imp_mod)
    imp_sim.atol = 1e-06
    imp_sim.rtol = 1e-06
    imp_sim.suppress_alg = True
    imp_sim.report_continuously = True
    imp_sim.make_consistent('IDA_YA_YDP_INIT')
    t, y, yd = imp_sim.simulate(5)
    nose.tools.assert_almost_equal(y[(-1)][0], 0.9401995, places=4)
    nose.tools.assert_almost_equal(y[(-1)][1], -0.34095124, places=4)
    nose.tools.assert_almost_equal(yd[(-1)][0], -0.88198927, places=4)
    nose.tools.assert_almost_equal(yd[(-1)][1], -2.43227069, places=4)
    nose.tools.assert_almost_equal(order[(-1)], 5, places=4)
    if with_plots:
        P.figure(1)
        P.plot(t, y, linestyle='dashed', marker='o')
        P.xlabel('Time')
        P.ylabel('State')
        P.title(imp_mod.name)
        P.figure(2)
        P.plot([0] + N.add.accumulate(N.diff(t)).tolist(), order)
        P.title('Used order during the integration')
        P.xlabel('Time')
        P.ylabel('Order')
        P.show()
    return (imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()