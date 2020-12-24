# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aid/quaternioning.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 1887 bytes
"""
quaternioning.py basic quaternion functions on 4D seqences

"""
from __future__ import absolute_import, division, print_function
import sys, math
from .sixing import *
from .consoling import getConsole
console = getConsole()

def qmag(q):
    """
    Returns the euclidean length or magnitude of quaternion q
    """
    return pow(sum(e * e for e in q), 0.5)


def qmag2(q):
    """
    Returns the euclidean length or magnitude of quaternion q squared
    """
    return sum(e * e for e in q)


def qconj(q):
    """
    Return quaduple (4 tuple) result of quaternion multiplation of q1 * q2
    Quaternion multiplication is not commutative  q1 * q2 != q2 * q1
    Quaternions q1 and q2 are sequences are of the form [w, x, y, z]
    """
    return tuple((-e if i > 0 else e) for i, e in enumerate(q))


def qnorm(q, check=False):
    """
    Returns normalized (euclidean norm) quaduple copy of quaternion quaduple q
    If q is zero quaternion then returns q as is

    For non zero q If check is True then and if qmag != 1.0 repeat normalization once
    """
    if not any(q):
        return q
    else:
        m = qmag(q)
        nq = tuple(e / m for e in q)
        if check:
            if qmag(nq) != 1.0:
                nq = qnorm(nq, check=check)
        return nq


def qmul(q1, q2):
    """
    Return quaduple (4 tuple) result of quaternion multiplation of q1 * q2
    Quaternion multiplication is not commutative  q1 * q2 != q2 * q1
    Quaternions q1 and q2 are sequences are of the form [w, x, y, z]
    """
    w = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
    x = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]
    y = q1[0] * q2[2] + q1[2] * q2[0] + q1[3] * q2[1] - q1[1] * q2[3]
    z = q1[0] * q2[3] + q1[3] * q2[0] + q1[1] * q2[2] - q1[2] * q2[1]
    return (w, x, y, z)