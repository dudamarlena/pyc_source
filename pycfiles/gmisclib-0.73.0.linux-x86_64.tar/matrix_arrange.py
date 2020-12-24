# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/matrix_arrange.py
# Compiled at: 2010-09-12 14:40:21
"""Take a covariance-like matrix, and re-order it to be close to a diagonal matrix.
We calculate a map that renames the indices (the same map for both left and right),
to bring large off-diagonal elements close to the diagonal.
"""
import math, random, numpy

def _eval_map(a, m, wt):
    """This is a measure of how far the matrix is from diagonal,
        after application of the mapping.
        Matrix "a" is a numeric python 2-d array.
        Map is a numeric python 1-d integer array."""
    n = a.shape[0]
    assert a.shape == (n, n)
    return numpy.sum(map_array(a, m) * wt)


def _offdiag(n):
    index = numpy.arange(n)
    offdiag = numpy.absolute(index[:, numpy.newaxis] - index[numpy.newaxis, :])
    assert offdiag.shape == (n, n)
    assert offdiag[(0, 0)] == 0
    assert offdiag[(1, 0)] == 1
    return offdiag


def _optimistic(n):
    return numpy.ones((n, n), numpy.int) - numpy.identity(n)


def diagonalize(a0):
    EPS = 1e-10
    a = numpy.array(a0, copy=True)
    n = a.shape[0]
    assert a.shape == (n, n)
    wt = numpy.square(_offdiag(n))
    m = numpy.arange(n)
    opval = _eval_map(a, m, _optimistic(n))
    bad = _eval_map(a, m, wt)
    bad0 = bad
    f = 1.0
    fr = math.pow(0.5, 1.0 / n)
    nobetter = 0
    while 1:
        i = random.randrange(n)
        j = random.randrange(n)
        if j == i:
            continue
        tmp = m[i]
        m[i] = m[j]
        m[j] = tmp
        bt = _eval_map(a, m, wt)
        if bt <= opval + bad * EPS:
            bad = bt
            break
        if bt <= bad * (1 + f / float(n)):
            if abs(bt - bad) > 0.1 * bad * f / float(n):
                f *= fr
                nobetter = 0
            bad = bt
            nobetter = 0
        else:
            tmp = m[i]
            m[i] = m[j]
            m[j] = tmp
            nobetter += 1
        if nobetter >= n * n:
            break

    if m[0] > m[(-1)]:
        m = m[::-1]
    return (
     m, bad0, bad)


def map_array(a, m):
    return numpy.take(numpy.take(a, m, axis=0), m, axis=1)


def test():
    a = numpy.array([[1, 0, 3, 2], [0, 1, 0, 0], [3, 0, 1, 0], [2, 0, 0, 1]])
    m, b0, b1 = diagonalize(a)
    assert b1 < b0
    print m
    print map_array(a, m)


if __name__ == '__main__':
    test()