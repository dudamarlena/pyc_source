# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/verify/mathHelpers.py
# Compiled at: 2018-08-17 21:53:27
import math

def is_NaN(x):
    if hasattr(x, 'is_NaN'):
        return x.is_NaN()
    return math.isnan(x)


def interval_aware_max(l):
    """
    max of two RealIntervalField elements is actually not giving the
    correct result.
    For example max(RIF(3.499,3.501),RIF(3.4,3.6)).endpoints() returns
    (3.499, 3.501) instead of (3.499, 3.6). Also, any NaN should trigger
    this to return NaN.

    This implements a correct max.
    """
    for i, x in enumerate(l):
        if is_NaN(x):
            return x
        if hasattr(x, 'max'):
            m = x
            for j, y in enumerate(l):
                if i != j:
                    if math.isnan(y):
                        return y
                    m = m.max(y)

            return m

    return max(l)


def interval_aware_min(l):
    """
    min of two RealIntervalField elements is actually not giving the correct
    result.
    For example min(RIF(3.499,3.501),RIF(3.4,3.6)).endpoints() returns
    (3.499, 3.501) instead of (3.4, 3.501). Also, any NaN should trigger
    this to return NaN.

    This implements a correct min.
    """
    for i, x in enumerate(l):
        if is_NaN(x):
            return x
        if hasattr(x, 'min'):
            m = x
            for j, y in enumerate(l):
                if i != j:
                    if math.isnan(y):
                        return y
                    m = m.min(y)

            return m

    return min(l)