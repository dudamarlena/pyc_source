# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/OaS.py
# Compiled at: 2017-10-03 13:07:16
"""Various utility functions etc. that don't obviously fit elsewhere.
"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip import ExceptionCpip

class ExceptionOas(ExceptionCpip):
    """Simple specialisation of an exception class for this module."""
    pass


def indexMatch(l, v):
    """Returns the index of v in sorted list l or -1.
    This uses Jon Bentley's binary search algorithm.
    This uses operators > and <."""
    i = 0
    j = len(l) - 1
    while i <= j:
        m = i + (j - i) // 2
        if l[m] < v:
            i = m + 1
        elif l[m] > v:
            j = m - 1
        else:
            return m

    return -1


def indexLB(l, v):
    """Returns the lower bound index in a sorted list l of the value that is
    equal to v or the nearest lower value to v.
    Returns -1 if l empty or all values higher than v."""
    TRACE = 0
    if TRACE:
        print 'TRACE indexLB(): l=%s, v=%s' % (l, v)
    i = 0
    j = len(l) - 1
    while i < j:
        m = i + (j - i) // 2
        if TRACE:
            print 'TRACE indexLB(): i=%d, j=%d, m=%d l[m]=%d' % (i, j, m, l[m])
        if m == i:
            if l[j] <= v:
                return j
            else:
                if l[i] <= v:
                    return i
                return -1

        if l[m] < v:
            i = m
        elif l[m] > v:
            j = m
        else:
            return m

    if TRACE:
        print 'TRACE indexLB(): END i=%d, j=%d' % (i, j)
    if i >= j and j >= 0 and j < len(l) and l[j] <= v:
        return j
    return -1


def indexUB(l, v):
    """Returns the upper bound index in a sorted list l of the value that is
    equal to v or the nearest upper value to v.
    Returns -1 if l empty or all values lower than v."""
    iLB = indexLB(l, v)
    if iLB == -1:
        if len(l) > 0:
            return 0
        else:
            return -1

    if l[iLB] == v:
        return iLB
    if iLB + 1 < len(l):
        return iLB + 1
    return -1