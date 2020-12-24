# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymills/mathtools.py
# Compiled at: 2013-07-27 09:03:17
__doc__ = 'Math Tools\n\nModule of small useful math tools aka common math routines.\n'
from math import sqrt

def mean(xs):
    """Calculate the mean of a list of numbers given by xs"""
    return sum(xs) / len(xs)


def std(xs):
    """Calculate the standard deviation of a list of numbers give by xs"""
    m = mean(xs)
    dxs = (x - m for x in xs)
    qdxs = (x * x for x in dxs)
    s = l = 0
    for i in qdxs:
        s += i
        l += 1

    return sqrt(s / (l - 1))