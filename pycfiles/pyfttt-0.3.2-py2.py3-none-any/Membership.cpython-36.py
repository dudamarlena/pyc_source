# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/common/Membership.py
# Compiled at: 2019-01-18 06:04:30
# Size of source mod 2**32: 2245 bytes
__doc__ = '\nMembership functions for Fuzzy Sets\n'
import numpy as np, math
from pyFTS import *

def trimf(x, parameters):
    """
    Triangular fuzzy membership function

    :param x: data point
    :param parameters: a list with 3 real values
    :return: the membership value of x given the parameters
    """
    xx = np.round(x, 3)
    if xx < parameters[0]:
        return 0
    if parameters[0] <= xx < parameters[1]:
        return (x - parameters[0]) / (parameters[1] - parameters[0])
    else:
        if parameters[1] <= xx <= parameters[2]:
            return (parameters[2] - xx) / (parameters[2] - parameters[1])
        return 0


def trapmf(x, parameters):
    """
    Trapezoidal fuzzy membership function

    :param x: data point
    :param parameters: a list with 4 real values
    :return: the membership value of x given the parameters
    """
    if x < parameters[0]:
        return 0
    else:
        if parameters[0] <= x < parameters[1]:
            return (x - parameters[0]) / (parameters[1] - parameters[0])
        else:
            if parameters[1] <= x <= parameters[2]:
                return 1
            if parameters[2] <= x <= parameters[3]:
                return (parameters[3] - x) / (parameters[3] - parameters[2])
        return 0


def gaussmf(x, parameters):
    """
    Gaussian fuzzy membership function

    :param x: data point
    :param parameters: a list with 2 real values (mean and variance)
    :return: the membership value of x given the parameters
    """
    return math.exp(-(x - parameters[0]) ** 2 / (2 * parameters[1] ** 2))


def bellmf(x, parameters):
    """
    Bell shaped membership function

    :param x:
    :param parameters:
    :return:
    """
    return 1 / (1 + abs((x - parameters[2]) / parameters[0]) ** (2 * parameters[1]))


def sigmf(x, parameters):
    """
    Sigmoid / Logistic membership function

    :param x:
    :param parameters: an list with 2 real values (smoothness and midpoint)
    :return
    """
    return 1 / (1 + math.exp(-parameters[0] * (x - parameters[1])))


def singleton(x, parameters):
    """
    Singleton membership function, a single value fuzzy function

    :param x:
    :param parameters: a list with one real value
    :returns
    """
    if x == parameters[0]:
        return 1
    else:
        return 0