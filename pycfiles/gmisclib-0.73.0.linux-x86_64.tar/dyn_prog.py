# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/dyn_prog.py
# Compiled at: 2010-02-15 15:19:26
"""Viterbi search"""
import numpy

def path(nodecost, linkcost):
    T = nodecost.shape[0]
    N = nodecost.shape[1]
    cost = numpy.zeros((N,))
    bestpathto = []
    for j in range(N):
        bestpathto.append([j])
        cost[j] = nodecost[(0, j)]

    for t in range(1, T):
        nbp = []
        ncost = numpy.zeros((N,))
        for j in range(N):
            cc = cost + linkcost[:, j]
            assert len(cc.shape) == 1
            o = numpy.argmin(cc)
            ncost[j] = cc[o] + nodecost[(t, j)]
            nbp.append(bestpathto[o] + [j])

        bestpathto = nbp
        cost = ncost

    assert len(cost.shape) == 1
    jj = numpy.argmin(cost)
    return (
     cost[jj], bestpathto[jj])


def test1():
    T = 10
    N = 7
    noc = numpy.zeros((T, N)) + 5
    noc[:, 3] = 1
    linkc = numpy.zeros((N, N)) + 2
    c, p = path(noc, linkc)
    assert abs(c - (10 + 18)) < 0.0001
    assert p == [3] * T


def test2():
    T = 10
    N = 7
    noc = numpy.zeros((T, N)) + 5
    for i in range(T):
        noc[(i, i % N)] = 1

    linkc = numpy.zeros((N, N)) + 2
    c, p = path(noc, linkc)
    assert abs(c - (10 + 18)) < 0.0001
    assert p == [0, 1, 2, 3, 4, 5, 6, 0, 1, 2]


def test3():
    T = 10
    N = 7
    noc = numpy.zeros((T, N)) + 1
    noc[(0, 0)] = 0
    linkc = numpy.zeros((N, N)) + 2
    for i in range(N):
        linkc[(i, (i + 1) % N)] = 1

    c, p = path(noc, linkc)
    assert abs(c - (0 + 9 + 9)) < 0.0001
    assert p == [0, 1, 2, 3, 4, 5, 6, 0, 1, 2]


if __name__ == '__main__':
    test1()
    test2()
    test3()