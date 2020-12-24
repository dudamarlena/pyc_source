# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/kinsol_with_jac.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import KINSOL
from assimulo.problem import Algebraic_Problem

def run_example(with_plots=True):
    """
    Example to demonstrate the use of the Sundials solver Kinsol with
    a user provided Jacobian.
    
    on return:
    
       - :dfn:`alg_mod`    problem instance
    
       - :dfn:`alg_solver`    solver instance
    
    """

    def res(y):
        r1 = 2 * y[0] + 3 * y[1] - 6
        r2 = 4 * y[0] + 9 * y[1] - 15
        return N.array([r1, r2])

    def jac(y):
        return N.array([[2.0, 3.0], [4.0, 9.0]])

    alg_mod = Algebraic_Problem(res, y0=[0, 0], jac=jac, name='KINSOL example with Jac')
    alg_solver = KINSOL(alg_mod)
    y = alg_solver.solve()
    nose.tools.assert_almost_equal(y[0], 1.5, 5)
    nose.tools.assert_almost_equal(y[1], 1.0, 5)
    return (
     alg_mod, alg_solver)


if __name__ == '__main__':
    mod, solv = run_example()