# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/tests/sample_sut_sin.py
# Compiled at: 2010-10-28 00:39:27
from math import radians, sin

def sut_sin(x):
    """
    Sample SUT used to demonstrate heuristic test oracles.
    """
    result = sin(radians(x))
    print 'sin(%f) = %s' % (x, result)
    return result