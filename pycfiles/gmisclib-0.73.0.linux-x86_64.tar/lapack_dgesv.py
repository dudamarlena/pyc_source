# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/lapack_dgesv.py
# Compiled at: 2007-08-13 06:22:59
import lapack_dge, Numeric

def _lg(n):
    k = 0
    twok = 1
    while twok < n:
        k += 1
        twok *= 2

    return k


def dgesv(a, b):
    """Solve a*x = b."""
    a = Numeric.array(a, Numeric.Float)
    b = Numeric.array(b, Numeric.Float)
    n = a.shape[0]
    assert a.shape == (n, n)
    nrhs = b.shape[1]
    assert b.shape == (n, nrhs)
    ipiv = Numeric.zeros((n,), Numeric.Int)
    info = 0
    o = lapack_dge.dgesv(n, nrhs, a, n, ipiv, b, n, info)
    assert o['info'] == 0
    return b


if __name__ == '__main__':
    a = Numeric.array([[2, 0], [0, 1]], Numeric.Float)
    b = Numeric.array([[1], [1]], Numeric.Float)
    print 'a=', a
    print 'b=', b
    print dgesv(a, b)