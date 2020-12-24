# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/sigmoids.py
# Compiled at: 2009-06-11 03:23:24
"""C functions."""
from numpy import exp, fabs

def sigmoid(x):
    return 1 / (1 + exp(-x))


def msigmoid(x):
    return 1 / (1 + exp(-(2.5 * x) ** 2))


def dsigmoid(x):
    return exp(-x) / (1 + exp(-x)) ** 2


def dmsigmoid(x):
    exponent = exp((2.5 * x) ** 2)
    return 12.5 * exponent * x / (1 + exponent) ** 2


dblsigmoid = lambda x: 2 * exp(x) / (1 + exp(x))

def mutability(x):
    return fabs(dmsigmoid(x))


def believing(x):
    return dsigmoid(x) * 4


def keyness(x):
    return dblsigmoid(x) * dsigmoid(x)