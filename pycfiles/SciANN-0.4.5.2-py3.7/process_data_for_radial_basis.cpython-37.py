# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/utils/process_data_for_radial_basis.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 1376 bytes
""" Process/Prepare standard data for the `Radial Basis Networks`.
"""
import numpy as np
from sklearn.neighbors import BallTree

def process_data_for_radial_basis(*args, **kwargs):
    """ Find closest point to each node in xs.

    # Arguments
        xs: A list of input vectors of dimension (N,1) with N as number of data-points.
        ys: A list of output vectors of dimension (N,1) with N as number of data-points.
        size_rb: Number of closest points.

    # Returns
        xrb: A list of `Radial Basis` inputs of dimension (N,size_rb) with N as number of data-points.
    """
    if len(args) == 2:
        xs = args[0]
        ys = None
        size_rb = args[1]
    else:
        if len(args) == 3:
            xs = args[0]
            ys = args[1]
            size_rb = args[2]
        else:
            raise ValueError
    if all([x.shape[(-1)] != 1 for x in xs]):
        for i, x in enumerate(xs):
            xs[i] = x.reshape(x.shape + (1, ))

    xsc = np.concatenate(xs, axis=(-1))
    tree = BallTree(xsc, size_rb)
    ids = tree.query(xsc, size_rb, return_distance=False)
    if 'return_ids' in kwargs:
        if kwargs['return_ids']:
            return ids
    xrbs = [x[ids].reshape(-1, size_rb) for x in xs]
    if ys is None:
        return xrbs
    yrbs = [y[ids].reshape(-1, size_rb) for y in ys]
    return (xrbs, yrbs)