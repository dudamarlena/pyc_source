# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/nonstationary/perturbation.py
# Compiled at: 2017-10-04 18:39:27
# Size of source mod 2**32: 438 bytes
__doc__ = '\nPertubation functions for Non Stationary Fuzzy Sets\n'
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