# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/logistic_map.py
# Compiled at: 2018-08-30 11:33:39
# Size of source mod 2**32: 615 bytes
__doc__ = '\nMay, Robert M. (1976). "Simple mathematical models with very complicated dynamics".\nNature. 261 (5560): 459–467. doi:10.1038/261459a0.\n\nx(t) = r * x(t-1) * (1 - x(t -1) )\n'
import numpy as np

def get_data(r=4, initial_value=0.3, iterations=100):
    """
    Return a list with the logistic map chaotic time series.

    :param r: Equation coefficient
    :param initial_value: Initial value of x. Default: 0.3
    :param iterations: number of iterations. Default: 100
    :return:
    """
    x = [
     initial_value]
    for t in np.arange(0, iterations):
        x.append(r * x[t] * (1 - x[t]))

    return x