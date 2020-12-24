# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fdtool\modules\ObtainEquivalences.py
# Compiled at: 2018-06-19 13:38:40
import binaryRepr

def f(C_km1, F, Closure, U):
    E = []
    for X in C_km1:
        for Y in F:
            if set(X).issubset(Closure[binaryRepr.toBin(list(Y[0]), U)]) and set(Y[0]).issubset(Closure[binaryRepr.toBin(X, U)]):
                if [tuple(X), Y[0]] not in E and [Y[0], tuple(X)] not in E and Y[0] != tuple(X):
                    E.append([tuple(X), Y[0]])

    return E