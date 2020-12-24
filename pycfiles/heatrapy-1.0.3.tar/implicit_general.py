# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: heatrapy/solvers/implicit_general.py
# Compiled at: 2018-03-01 08:27:13
from __future__ import unicode_literals
import numpy as np, copy

def implicit_general(obj):
    """implicit_general solver.

    Used to compute one time step of systems with fixed thermal contuctivity.

    """
    a = np.zeros((obj.num_points, obj.num_points))
    b = np.zeros(obj.num_points)
    a[0][0] = 1
    if obj.boundaries[0] == 0:
        b[0] = obj.temperature[1][0]
    else:
        b[0] = obj.boundaries[0]
    a[(obj.num_points - 1)][obj.num_points - 1] = 1
    if obj.boundaries[1] == 0:
        value = obj.temperature[(obj.num_points - 2)][0]
        b[obj.num_points - 1] = value
    else:
        b[obj.num_points - 1] = obj.boundaries[1]
    for i in range(1, obj.num_points - 1):
        beta = obj.k[i] * obj.dt / (2 * obj.rho[i] * obj.Cp[i] * obj.dx * obj.dx)
        sigma = obj.dt / (obj.rho[i] * obj.Cp[i])
        a[i][i - 1] = -beta
        a[i][i] = 1 + 2 * beta - sigma * obj.Q[i]
        a[i][i + 1] = -beta
        b[i] = (1 - 2 * beta - sigma * obj.Q[i]) * obj.temperature[i][0] + beta * obj.temperature[(i + 1)][0] + beta * obj.temperature[(i - 1)][0] + 2.0 * sigma * (obj.Q0[i] - obj.Q[i] * obj.amb_temperature)

    x = np.linalg.solve(a, b)
    y = copy.copy(obj.temperature)
    for i in range(obj.num_points):
        y[i][1] = x[i]
        y[i][0] = x[i]

    return y