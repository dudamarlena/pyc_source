# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/useless_functions.py
# Compiled at: 2018-04-13 18:30:00
# Size of source mod 2**32: 1187 bytes
""" Ce module contient de multiples fonctions ainsi que leurs dérivées utiles
à la descente de gradient.
"""
import numpy as np

def xcosx_1D(x):
    """ Return the value of the xcosx function. """
    return x * np.cos(x)


def xcosx_1D_d(x):
    """ Return the value of the xcosx function's derivative. """
    return np.cos(x) - x * np.sin(x)


def minuslogxxtwo_1D(x):
    """ Return the value of the minuslogxxtwo function. """
    return -np.log(x) + np.power(x, 2)


def minuslogxxtwo_1D_d(x):
    """ Return the value of the minuslogxxtwo function's derivative. """
    return -(1 / x) + 2 * x


def rosenbrock_2D(x1, x2):
    """ Return the value of the Rosenbrock function. """
    return 100 * np.power(x2 - np.power(x1, 2), 2) + np.power(1 - x1, 2)


def rosenbrock_2D_d(x1, x2):
    """ Return the value of the Rosenbrock function's derivative. """
    return (
     100 * (-4 * x2 * x1 + 4 * x1 ** 3) + (-2 * x1 + 2 * x1),
     2 * x2 - 2 * x1 ** 2)


if __name__ == '__main__':
    pass