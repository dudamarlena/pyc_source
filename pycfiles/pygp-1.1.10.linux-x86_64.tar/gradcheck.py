# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/gradcheck.py
# Compiled at: 2013-04-10 06:45:39
""" cheeck for covarince matrices"""
import scipy as SP
relchange = 1e-05

def grad_check_logtheta(K, logtheta, x0, dimensions=None):
    """perform grad check with respect to hyperparameters logtheta"""
    x1 = logtheta.copy()
    n = x1.shape[0]
    nx = x0.shape[0]
    diff = SP.zeros([n, nx, nx])
    for i in xrange(n):
        change = relchange * x1[i]
        change = max(change, 1e-05)
        x1[i] = logtheta[i] + change
        Lplus = K.K(x1, x0, x0)
        x1[i] = logtheta[i] - change
        Lminus = K.K(x1, x0, x0)
        x1[i] = logtheta[i]
        diff[i, :, :] = (Lplus - Lminus) / (2.0 * change)

    ana = SP.zeros([n, nx, nx])
    for iid in xrange(n):
        ana[iid, :, :] = K.Kgrad_theta(x1, x0, iid)

    delta = (ana - diff) / (diff + 1e-10)
    print 'delta %.2f' % SP.absolute(delta).max()
    try:
        import ipdb
        ipdb.set_trace()
    except:
        import pdb
        pdb.set_trace()


def grad_check_Kx(K, logtheta, x0, dimensions=None):
    """perform grad check with respect to input x"""
    x1 = x0.copy()
    n = x1.shape[0]
    if dimensions is None:
        dimensions = SP.arange(x0.shape[1])
    nd = len(dimensions)
    diff = SP.zeros([n, nd, n, n])
    for i in xrange(n):
        for iid in xrange(nd):
            d = dimensions[iid]
            change = relchange * x0[(i, d)]
            change = max(change, 1e-05)
            x1[(i, d)] = x0[(i, d)] + change
            Lplus = K.K(logtheta, x1, x1)
            x1[(i, d)] = x0[(i, d)] - change
            Lminus = K.K(logtheta, x1, x1)
            x1[(i, d)] = x0[(i, d)]
            diff[i, iid, :, :] = (Lplus - Lminus) / (2.0 * change)

    ana = SP.zeros([n, nd, n, n])
    for iid in xrange(nd):
        d = dimensions[iid]
        dKx = K.Kgrad_x(logtheta, x1, x1, d)
        for iin in xrange(n):
            dKxn = SP.zeros([n, n])
            dKxn[iin, :] = 1.0 * dKx[iin, :]
            dKxn[:, iin] += 1.0 * dKx[iin, :]
            ana[iin, iid, :, :] = dKxn

    delta = ((ana - diff) ** 2).sum()
    print 'delta %.2f' % SP.absolute(delta).max()
    try:
        import ipdb
        ipdb.set_trace()
    except:
        import pdb
        pdb.set_trace()

    return