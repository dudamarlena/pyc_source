# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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