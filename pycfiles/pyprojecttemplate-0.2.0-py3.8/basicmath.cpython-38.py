# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyprojecttemplate\basicmath.py
# Compiled at: 2019-12-16 00:13:18
# Size of source mod 2**32: 406 bytes
"""
Basic Sample Python to define common mathematical functions
"""
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