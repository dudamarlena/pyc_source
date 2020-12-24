# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyprojecttemplate\basicmath.py
# Compiled at: 2019-12-16 00:13:18
# Size of source mod 2**32: 406 bytes
__doc__ = '\nBasic Sample Python to define common mathematical functions\n'
import math

def calculate_square(num):
    """
    Returns the square of a given number
    """
    return num * num


def add(a, b):
    """
    Returns the sum of two numbers
    """
    return a + b


def calculate_sin(x):
    """
    Return the sine of x (measured in radians).
    """
    return math.sin(x)