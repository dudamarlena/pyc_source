# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/triangle.py
# Compiled at: 2008-04-20 13:19:45
"""some triangle functions

given a triangle OAB, calculate some reuslt from some given.

angle's unit is radian not degree.

if failed, return None
"""
import math

def calc_ab(oa, ob, aob):
    """calc_ab(oa, ob, aob) -> float
    given OA, OB and angle AOB, calculate AB
    angle's unit is radian not degree.

    for example:
    >>> calc_ab(3,4,math.radians(90)) == 5
    True
    """
    return math.sqrt(oa * oa + ob * ob - 2 * oa * ob * math.cos(aob))


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()