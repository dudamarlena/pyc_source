# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\PyKrige\variogram_models.py
# Compiled at: 2016-01-05 13:51:40
# Size of source mod 2**32: 2126 bytes
"""Code by Benjamin S. Murphy
bscott.murphy@gmail.com

Dependencies:
    numpy

Methods:
    linear_variogram_model(params, dist):
        params (array-like): [slope, nugget]
        dist (array-like): Points at which to calculate variogram model.
    power_variogram_model(params, dist):
        params (array-like): [scale, exponent, nugget]
        dist (array-like): Points at which to calculate variogram model.
    gaussian_variogram_model(params, dist):
        params (array-like): [sill, range, nugget]
        dist (array-like): Points at which to calculate variogram model.
    exponential_variogram_model(params, dist):
        params (array-like): [sill, range, nugget]
        dist (array-like): Points at which to calculate variogram model.
    spherical_variogram_model(params, dist):
        params (array-like): [sill, range, nugget]
        dist (array-like): Points at which to calculate variogram model.

References:
    P.K. Kitanidis, Introduction to Geostatistcs: Applications in Hydrogeology,
    (Cambridge University Press, 1997) 272 p.

Copyright (c) 2015 Benjamin S. Murphy
"""
import numpy as np

def linear_variogram_model(params, dist):
    return float(params[0]) * dist + float(params[1])


def power_variogram_model(params, dist):
    return float(params[0]) * dist ** float(params[1]) + float(params[2])


def gaussian_variogram_model(params, dist):
    return (float(params[0]) - float(params[2])) * (1 - np.exp(-dist ** 2 / (float(params[1]) * 4.0 / 7.0) ** 2)) + float(params[2])


def exponential_variogram_model(params, dist):
    return (float(params[0]) - float(params[2])) * (1 - np.exp(-dist / (float(params[1]) / 3.0))) + float(params[2])


def spherical_variogram_model(params, dist):
    return np.piecewise(dist, [dist <= float(params[1]), dist > float(params[1])], [
     lambda x: (float(params[0]) - float(params[2])) * (3 * x / (2 * float(params[1])) - x ** 3 / (2 * float(params[1]) ** 3)) + float(params[2]),
     float(params[0])])