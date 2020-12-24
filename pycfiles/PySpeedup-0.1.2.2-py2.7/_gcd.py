# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_gcd.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup import concurrent

@concurrent.Cache
def gcd(a, b):
    """Using the extended Euclidean algorithm, finds the gcd between a and b.

    For example::

        >>> gcd(5,10)
        5
        >>> gcd(1024,768)
        256
        >>> gcd(1474038573,183508437983)
        1

    """
    r = a % b
    if r == 0:
        return b
    else:
        return gcd(b, r)


if __name__ == '__main__':
    import doctest
    doctest.testmod()