# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/medpolish.py
# Compiled at: 2010-07-13 12:32:48
import numpy
from numpy import median
from mpgutils import utils
maxiter = 10
eps = 0.01

def npmedian(x):
    """Dear numPY.  Please don't change your APIs, so I don't have to wrap them."""
    nv = numpy.__version__
    if nv == '1.0.1' or nv == '1.0.4' or nv == '1.1' or nv == '1.1.1':
        return median(x)
    return median(x, axis=0)


def medpolish(x):
    z = x.copy()
    (nrows, ncols) = z.shape
    t = 0
    r = numpy.zeros(nrows, dtype='f')
    c = numpy.zeros(ncols, dtype='f')
    oldsum = 0
    converged = 0
    for iter in range(1, maxiter + 1):
        rdelta = npmedian(z.transpose())
        r = r + rdelta
        rdelta.shape = (nrows, 1)
        z = z - utils.repmat(rdelta, 1, ncols)
        delta = npmedian(c)
        c = c - delta
        t = t + delta
        cdelta = npmedian(z)
        c = c + cdelta
        cdelta.shape = (1, ncols)
        z = z - utils.repmat(cdelta, nrows, 1)
        delta = npmedian(r)
        r = r - delta
        t = t + delta
        newsum = sum(sum(abs(z)))
        if newsum == 0 or abs(newsum - oldsum) < eps * newsum:
            converged = 1
        if converged:
            break
        oldsum = newsum

    return (t, r, c, z)