# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/resample.py
# Compiled at: 2007-08-13 06:22:59
"""Resample a time series by a factor r.  I.e. sample more
densely (r<1) or less densely (r>1).
Also see tsops.py."""
import Num

def simple(a, r, direction=0):
    aa = Num.array(a)
    newlen = 1 + int((aa.shape[direction] - 1) / r)
    t = Num.around(Num.arrayrange(newlen) * r)
    aswap = Num.swapaxes(aa, direction, 0)
    interped = Num.choose(t, aswap)
    return Num.swapaxes(interped, direction, 0)


def compare(a, b):
    assert len(a) == len(b)
    for i in range(len(a)):
        assert a[i] == b[i]


def test():
    x = simple([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2.0)
    compare(x, [0, 2, 4, 6, 8])
    x = simple([0, 1, 2, 3, 4], 0.5)
    compare(x, [0, 1, 1, 2, 2, 3, 3, 4, 4])


if __name__ == '__main__':
    test()