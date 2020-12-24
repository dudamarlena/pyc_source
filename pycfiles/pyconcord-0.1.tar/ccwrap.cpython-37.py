# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/task/concord/ccwrap.py
# Compiled at: 2019-11-20 08:33:30
# Size of source mod 2**32: 636 bytes


def concord(x, penalty1, penalty2=0, x0=None, epstol=1e-05, maxitr=100, bb=0):
    from .ccista import ccista
    from scipy.sparse import identity, coo_matrix, csr_matrix
    from numpy import vstack
    n, p = x.shape
    if x0 is None:
        x0 = identity(p).tocoo()
    else:
        if type(x0) is not coo_matrix:
            try:
                x0 = x0.tocoo()
            except:
                raise Exception('x0 is not convertible to COO sparse matrix')

    i, j, data = ccista(x, x0.row, x0.col, x0.data, penalty1, penalty2, epstol, maxitr, bb)
    return csr_matrix((data, vstack((i, j))), shape=(
     p, p))