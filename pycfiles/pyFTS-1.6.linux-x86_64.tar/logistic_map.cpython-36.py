# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/data/logistic_map.py
# Compiled at: 2018-08-30 11:33:39
# Size of source mod 2**32: 615 bytes
"""
May, Robert M. (1976). "Simple mathematical models with very complicated dynamics".
Nature. 261 (5560): 459–467. doi:10.1038/261459a0.

x(t) = r * x(t-1) * (1 - x(t -1) )
"""
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