# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/tikhonov.py
# Compiled at: 2018-05-17 05:55:18
from math import fabs

def tikhonov(value, refcurv=610000.0, alpha=1e-08):

    def computeCurvature(bin):
        return value[(bin - 1)] - 2.0 * value[bin] + value[(bin + 1)]

    curvature = sum([ c * c for c in map(computeCurvature, range(1, len(value) - 1))
                    ])
    deltaCurv = fabs(curvature - refcurv)
    return -deltaCurv * alpha