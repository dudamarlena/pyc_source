# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLBezoutEquation.py
# Compiled at: 2018-04-23 08:51:10
from .NTLEuclideanAlgorithm import euclideanAlgorithm
from .NTLPolynomial import Polynomial
from .NTLValidations import int_check
__all__ = [
 'bezoutEquation', 'coefficient_s', 'coefficient_t']
nickname = 'bezout'

def bezoutEquation(a, b):
    exflag = pn_a = pn_b = False
    if isinstance(a, Polynomial) or isinstance(b, Polynomial):
        a = Polynomial(a)
        b = Polynomial(b)
    else:
        int_check(a, b)
        if a < 0:
            a *= -1
            pn_a = True
        if b < 0:
            b *= -1
            pn_b = True
        if a < b:
            a, b = b, a
            pn_a, pn_b = pn_b, pn_a
            exflag = True
    q = [
     0] + euclideanAlgorithm(a, b)
    s, t = coefficients(q)
    if pn_a ^ pn_b:
        if exflag:
            tmp = s
            s = -t if pn_b else t
            t = -tmp if pn_a else tmp
        else:
            if pn_b:
                s = -s
            if pn_a:
                t = -t
    elif pn_a and pn_b:
        if exflag:
            s, t = -t, -s
        else:
            s, t = -s, -t
    elif exflag:
        s, t = t, s
    return (
     s, t)


def coefficients(q):
    s_j1 = 1
    s_j2 = 0
    t_j1 = 0
    t_j2 = 1
    for q_j in q:
        s_j = -q_j * s_j1 + s_j2
        t_j = -q_j * t_j1 + t_j2
        s_j2 = s_j1
        s_j1 = s_j
        t_j2 = t_j1
        t_j1 = t_j
    else:
        return (
         s_j, t_j)

    return (0, 1)