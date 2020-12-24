# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/recovery.py
# Compiled at: 2010-09-17 11:05:27
"""
Recovery experiment with learned dual dictionaries.
"""
import sys, numpy as NP, numpy.random as RA, pylab
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python %s path-to-dictionary-file' % sys.argv[0]
        sys.exit(0)
    npz = NP.load(sys.argv[1])
    D, C = npz['D'], npz['C']
    (d, K) = D.shape
    n = 50
    N = n * (K - 1)
    U0 = RA.normal(size=(K, N))
    X = NP.zeros((d, N))
    for i in xrange(1, K):
        for j in xrange(n):
            U0[(RA.permutation(K)[i:], j + (i - 1) * n)] = 0

    S = NP.where(NP.abs(U0) > 0, 1, 0)
    s = NP.sum(S, 0)
    assert s.min() == 1, s
    assert s.max() == K - 1, s
    X = NP.dot(D, U0)
    U = NP.dot(C, X)
    I = NP.argsort(NP.abs(U), 0)[::-1, :]
    r = []
    for i in xrange(1, K):
        cols = NP.indices((i, n))[1]
        r.append(S[(I[:i, (i - 1) * n:i * n], cols)].astype(NP.float).mean())

    pylab.plot(NP.arange(1, K), r)
    pylab.show()