# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/kinsol_basic.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import KINSOL
from assimulo.problem import Algebraic_Problem

def run_example(with_plots=True):
    """
    Example to demonstrate the use of the Sundials solver Kinsol
    for the simple equation :math:`0 = 1 - y`
    
    on return:
    
       - :dfn:`alg_mod`    problem instance
    
       - :dfn:`alg_solver`    solver instance
    
    """

    def res(y):
        return 1 - y

    alg_mod = Algebraic_Problem(res, y0=0, name='Simple KINSOL Example')
    alg_solver = KINSOL(alg_mod)
    y = alg_solver.solve()
    nose.tools.assert_almost_equal(y, 1.0, 5)
    return (
     alg_mod, alg_solver)


if __name__ == '__main__':
    mod, solv = run_example()