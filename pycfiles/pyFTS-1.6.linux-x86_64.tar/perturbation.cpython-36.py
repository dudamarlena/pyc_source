# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/nonstationary/perturbation.py
# Compiled at: 2017-10-04 18:39:27
# Size of source mod 2**32: 438 bytes
"""
Pertubation functions for Non Stationary Fuzzy Sets
"""
import numpy as np
from pyFTS import *
from pyFTS.common import FuzzySet, Membership

def linear(x, parameters):
    return np.polyval(parameters, x)


def polynomial(x, parameters):
    return np.polyval(parameters, x)


def exponential(x, parameters):
    return np.exp(x * parameters[0])


def periodic(x, parameters):
    return parameters[0] * np.sin(x * parameters[1])