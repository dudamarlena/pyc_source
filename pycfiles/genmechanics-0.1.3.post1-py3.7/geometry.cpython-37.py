# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genmechanics/geometry.py
# Compiled at: 2020-03-26 14:17:33
# Size of source mod 2**32: 1524 bytes
"""
Created on Wed Nov 16 11:44:25 2016

@author: steven
"""
import numpy as npy, math
import scipy.linalg as linalg

def CrossProductMatrix(u):
    L = npy.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])
    return L


def Euler2TransferMatrix(psi, theta, phi):
    """
    Give Transition Matrix from euler angles
    Angles in radians
    """
    cpsi = math.cos(psi)
    spsi = math.sin(psi)
    ctheta = math.cos(theta)
    stheta = math.sin(theta)
    cphi = math.cos(phi)
    sphi = math.sin(phi)
    P = npy.array([[cphi * cpsi - sphi * ctheta * spsi, -spsi * cphi - cpsi * ctheta * sphi, stheta * sphi], [cpsi * sphi + spsi * ctheta * cphi, -sphi * spsi + cphi * ctheta * cpsi, -stheta * cphi], [spsi * stheta, cpsi * stheta, ctheta]])
    return P


def TransferMatrix2Euler(R):
    if (R[(2, 2)] != 1) & (R[(2, 2)] != -1):
        theta = math.acos(R[(2, 2)])
        psi = math.atan2(R[(2, 0)] / math.sin(theta), R[(2, 1)] / math.sin(theta))
        phi = math.atan2(R[(0, 2)] / math.sin(theta), -R[(1, 2)] / math.sin(theta))
    else:
        phi = 0
        if R[(2, 2)] == 1:
            theta = 0
            psi = math.atan2(R[(1, 0)], R[(0, 0)])
        else:
            theta = math.pi
            psi = -math.atan2(R[(1, 0)], R[(0, 0)])
    return npy.array([psi, theta, phi])


def Direction2Euler(u, v=npy.random.random(3)):
    u = u / linalg.norm(u)
    R = npy.zeros((3, 3))
    R[:, 0] = u
    v = v - npy.dot(u, v) * u
    v = v / linalg.norm(v)
    w = npy.cross(u, v)
    R[:, 1] = v
    R[:, 2] = w
    euler = TransferMatrix2Euler(R)
    return euler