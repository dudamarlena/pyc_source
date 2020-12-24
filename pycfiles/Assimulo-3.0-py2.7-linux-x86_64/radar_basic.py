# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/radar_basic.py
# Compiled at: 2017-12-28 04:09:42
"""
Created on Tue Feb 21 14:03:12 2012
@author: tony
"""
from scipy import *
from matplotlib.pyplot import *
from copy import copy, deepcopy
from assimulo.problem import Delay_Explicit_Problem
from assimulo.solvers import radar5

class Simple(Delay_Explicit_Problem):

    def __init__(self):
        Delay_Explicit_Problem.__init__(self)
        self.lagcompmap = [[0]]

    def time_lags(self, t, y):
        return [
         t - 1.0]

    def rhs(self, t, y, ydelay):
        ytm1 = ydelay[0][0]
        return -y + ytm1

    def phi(self, i, t):
        return sin(pi * t)


if __name__ == '__main__':
    RTOL = 1e-06
    ATOL = 1e-06
    H = 0.001
    mxst = 1000
    p = Simple()
    p.y0 = 0
    t0 = 0
    tf = 5.0
    s = radar5.Radar5ODE(p)
    s.grid = array([1.0])
    s.grid = array([0.5, 2.1])
    s.grid = array([0.7, 1.0, 1.1])
    s.grid = array([0.7, 1.0, 1.1, 2.5, 3.7, 4.3])
    s.rtol = RTOL
    s.atol = ATOL
    s.mxst = mxst
    s.inith = H
    s.maxsteps = 1000
    t, y = s.simulate(tf)
    y1 = array(deepcopy(s.y_sol)).reshape(-1)
    t1 = copy(s.t_sol)
    past1 = deepcopy(s.past)