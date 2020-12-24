# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/cvode_gyro.py
# Compiled at: 2017-12-28 04:09:42
from scipy import *
import pylab as P, nose
from assimulo.problem import Explicit_Problem
from assimulo.solvers import CVode

def run_example(with_plots=True):
    """
    Simulations for the Gyro (Heavy Top) example in Celledoni/Safstrom: 
        Journal of Physics A, Vol 39, 5463-5478, 2006
        
    on return:
    
       - :dfn:`exp_mod`    problem instance
    
       - :dfn:`exp_sim`    solver instance
    
    """

    def curl(v):
        return array([[0, v[2], -v[1]], [-v[2], 0, v[0]], [v[1], -v[0], 0]])

    def f(t, u):
        """
        Simulations for the Gyro (Heavy Top) example in Celledoni/Safstrom: 
        Journal of Physics A, Vol 39, 5463-5478, 2006
        """
        I1 = 1000.0
        I2 = 5000.0
        I3 = 6000.0
        u0 = [0, 0, 1.0]
        pi = u[0:3]
        Q = u[3:12].reshape((3, 3))
        Qu0 = dot(Q, u0)
        f = array([Qu0[1], -Qu0[0], 0.0])
        f = 0
        omega = array([pi[0] / I1, pi[1] / I2, pi[2] / I3])
        pid = dot(curl(omega), pi) + f
        Qd = dot(curl(omega), Q)
        return hstack([pid, Qd.reshape((9, ))])

    def energi(state):
        energi = []
        for st in state:
            Q = st[3:12].reshape((3, 3))
            pi = st[0:3]
            u0 = [0, 0, 1.0]
            Qu0 = dot(Q, u0)
            V = Qu0[2]
            T = 0.5 * (pi[0] ** 2 / 1000.0 + pi[1] ** 2 / 5000.0 + pi[2] ** 2 / 6000.0)
            energi.append([T])

        return energi

    y0 = hstack([[10000.0, 50000.0, 60000], eye(3).reshape((9, ))])
    exp_mod = Explicit_Problem(f, y0, name='Gyroscope Example')
    exp_sim = CVode(exp_mod)
    exp_sim.discr = 'BDF'
    exp_sim.iter = 'Newton'
    exp_sim.maxord = 2
    exp_sim.atol = 1e-10
    exp_sim.rtol = 1e-10
    t, y = exp_sim.simulate(0.1)
    nose.tools.assert_almost_equal(y[(-1)][0], 692.800241862)
    nose.tools.assert_almost_equal(y[(-1)][8], 0.708468221)
    if with_plots:
        P.plot(t, y / 10000.0)
        P.xlabel('Time')
        P.ylabel('States, scaled by $10^4$')
        P.title(exp_mod.name)
        P.show()
    return (exp_mod, exp_sim)


if __name__ == '__main__':
    mod, sim = run_example()