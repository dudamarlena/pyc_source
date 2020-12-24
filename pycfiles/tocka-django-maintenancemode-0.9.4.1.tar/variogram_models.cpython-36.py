# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\PyKrige\variogram_models.py
# Compiled at: 2016-01-05 13:51:40
# Size of source mod 2**32: 2126 bytes
__doc__ = 'Code by Benjamin S. Murphy\nbscott.murphy@gmail.com\n\nDependencies:\n    numpy\n\nMethods:\n    linear_variogram_model(params, dist):\n        params (array-like): [slope, nugget]\n        dist (array-like): Points at which to calculate variogram model.\n    power_variogram_model(params, dist):\n        params (array-like): [scale, exponent, nugget]\n        dist (array-like): Points at which to calculate variogram model.\n    gaussian_variogram_model(params, dist):\n        params (array-like): [sill, range, nugget]\n        dist (array-like): Points at which to calculate variogram model.\n    exponential_variogram_model(params, dist):\n        params (array-like): [sill, range, nugget]\n        dist (array-like): Points at which to calculate variogram model.\n    spherical_variogram_model(params, dist):\n        params (array-like): [sill, range, nugget]\n        dist (array-like): Points at which to calculate variogram model.\n\nReferences:\n    P.K. Kitanidis, Introduction to Geostatistcs: Applications in Hydrogeology,\n    (Cambridge University Press, 1997) 272 p.\n\nCopyright (c) 2015 Benjamin S. Murphy\n'
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