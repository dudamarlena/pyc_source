# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/ida_with_jac_spgmr.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, nose
from assimulo.solvers import IDA
from assimulo.problem import Implicit_Problem

def run_example(with_plots=True):
    r"""
    An example for IDA with scaled preconditioned GMRES method
    as a special linear solver.
    Note, how the operation Jacobian times vector is provided.
    
    ODE:
    
    .. math::
       
       \dot y_1 - y_2 &= 0\\
       \dot y_2 -9.82 &= 0
       
    
    on return:
    
       - :dfn:`imp_mod`    problem instance
    
       - :dfn:`imp_sim`    solver instance
       
    """

    def res(t, y, yd):
        res_0 = yd[0] - y[1]
        res_1 = yd[1] + 9.82
        return N.array([res_0, res_1])

    def jacv(t, y, yd, res, v, c):
        jy = N.array([[0, -1.0], [0, 0]])
        jyd = N.array([[1, 0.0], [0, 1]])
        j = jy + c * jyd
        return N.dot(j, v)

    y0 = [
     1.0, 0.0]
    yd0 = [0.0, -9.82]
    imp_mod = Implicit_Problem(res, y0, yd0, name='Example using the Jacobian Vector product')
    imp_mod.jacv = jacv
    imp_sim = IDA(imp_mod)
    imp_sim.atol = 1e-05
    imp_sim.rtol = 1e-05
    imp_sim.linear_solver = 'SPGMR'
    t, y, yd = imp_sim.simulate(5, 1000)
    nose.tools.assert_almost_equal(y[(-1)][0], -121.75, 4)
    nose.tools.assert_almost_equal(y[(-1)][1], -49.1)
    if with_plots:
        P.plot(t, y)
        P.xlabel('Time')
        P.ylabel('State')
        P.title(imp_mod.name)
        P.show()
    return (
     imp_mod, imp_sim)


if __name__ == '__main__':
    mod, sim = run_example()