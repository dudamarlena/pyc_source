# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/tests/sample_sut_sin_error.py
# Compiled at: 2010-10-28 01:11:57
from math import radians, sin

def sut_sin_error(x):
    """
    Sample SUT used to demonstrate heuristic test oracles.
    """
    if x < 120.0 or 140.0 <= x:
        result = sin(radians(x))
    else:
        result = -sin(radians(x))
    return result