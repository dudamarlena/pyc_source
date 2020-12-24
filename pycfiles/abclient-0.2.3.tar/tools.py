# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/taghawi/Dropbox/workspace/abce/unittest/tools.py
# Compiled at: 2017-05-30 09:27:14
__doc__ = ' This file contains functions to compare floating point variables to 0. All\nvariables in this simulation as in every computer programm are floating\npoint variables. Floating point variables are not exact. Therefore var_a == var_b\nhas no meaning. Further a variable that is var_c = 9.999999999999966e-30 is for our\npurpose equal to zero, but var_c == 0 would lead to False.\n:meth:`is_zero`, :meth:`is_positive` and :meth:`is_negative` work\naround this problem by defining float epsilon and determine whether the variable is\nsufficiently close to zero or not.\n\nThis file also defines the :exc:`tools.NotEnoughGoods`\n'
from __future__ import division
epsilon = 1e-06

def is_zero(x):
    """ checks whether a number is sufficiently close to zero. All variables
    in ABCE are floating point numbers. Due to the workings of floating point
    arithmetic. If x is 1.0*e^-100 so really close to 0, x == 0 will be false;
    is_zero will be true.
    """
    return -epsilon < x < epsilon


def is_positive(x):
    """ checks whether a number is positive and sufficiently different from
    zero. All variables in ABCE are floating point numbers. Due to the workings
    of floating point arithmetic. If x is 1.0*e^-100 so really close to 0,
    x > 0 will be true, eventhough it is very very small;
    is_zero will be true.
    """
    return -epsilon <= x


def is_negative(x):
    """ see is positive """
    return x <= epsilon