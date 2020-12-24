# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: heatrapy/solvers/implicit_k.py
# Compiled at: 2018-03-01 11:04:31
"""Contains the implicit_k solver.

Used to compute thermal processes

"""
import numpy as np, copy

def implicit_k(obj):
    """implicit_k solver.

    Used to compute one time step of systems with k-dependent thermal
    contuctivity.

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
        gamma = 4.0 * obj.rho[i] * obj.Cp[i] * obj.dx * obj.dx / obj.dt
        a[i][i - 1] = obj.k[(i - 1)] + obj.k[i]
        a[i][i] = -(gamma + obj.k[(i + 1)] + obj.k[(i - 1)] + 2.0 * obj.k[i] - 2 * obj.dt * obj.dt * obj.Q[i])
        a[i][i + 1] = obj.k[(i + 1)] + obj.k[i]
        b[i] = -(obj.k[(i + 1)] + obj.k[i]) * obj.temperature[(i + 1)][0] + (-gamma + obj.k[(i + 1)] + obj.k[(i - 1)] + 2.0 * obj.k[i] - 2 * obj.dt * obj.dt * obj.Q[i]) * obj.temperature[i][0] - (obj.k[(i - 1)] + obj.k[i]) * obj.temperature[(i - 1)][0] - 4.0 * obj.dx * obj.dx * (obj.Q0[i] - obj.Q[i] * obj.amb_temperature)

    x = np.linalg.solve(a, b)
    y = copy.copy(obj.temperature)
    for i in range(obj.num_points):
        y[i][1] = x[i]
        y[i][0] = x[i]

    return y