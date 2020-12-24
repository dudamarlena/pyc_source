# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/ce_util.py
# Compiled at: 2018-05-14 00:27:06
# Size of source mod 2**32: 3142 bytes
"""
Utility functions used in CompEcon

Based routines found in the CompEcon toolbox by Miranda and Fackler.

References
----------
Miranda, Mario J, and Paul L Fackler. Applied Computational Economics
and Finance, MIT Press, 2002.

"""
from functools import reduce
import numpy as np

def ckron(*arrays):
    """
    Repeatedly applies the np.kron function to an arbitrary number of
    input arrays

    Parameters
    ----------
    *arrays : tuple/list of np.ndarray

    Returns
    -------
    out : np.ndarray
          The result of repeated kronecker products.

    Notes
    -----
    Based of original function `ckron` in CompEcon toolbox by Miranda
    and Fackler.

    References
    ----------
    Miranda, Mario J, and Paul L Fackler. Applied Computational
    Economics and Finance, MIT Press, 2002.

    """
    return reduce(np.kron, arrays)


def gridmake(*arrays):
    """
    Expands one or more vectors (or matrices) into a matrix where rows span the
    cartesian product of combinations of the input arrays. Each column of the
    input arrays will correspond to one column of the output matrix.

    Parameters
    ----------
    *arrays : tuple/list of np.ndarray
              Tuple/list of vectors to be expanded.

    Returns
    -------
    out : np.ndarray
          The cartesian product of combinations of the input arrays.

    Notes
    -----
    Based of original function ``gridmake`` in CompEcon toolbox by
    Miranda and Fackler

    References
    ----------
    Miranda, Mario J, and Paul L Fackler. Applied Computational Economics
    and Finance, MIT Press, 2002.

    """
    if all([i.ndim == 1 for i in arrays]):
        d = len(arrays)
        if d == 2:
            out = _gridmake2(*arrays)
        else:
            out = _gridmake2(arrays[0], arrays[1])
            for arr in arrays[2:]:
                out = _gridmake2(out, arr)

        return out
    raise NotImplementedError('Come back here')


def _gridmake2(x1, x2):
    """
    Expands two vectors (or matrices) into a matrix where rows span the
    cartesian product of combinations of the input arrays. Each column of the
    input arrays will correspond to one column of the output matrix.

    Parameters
    ----------
    x1 : np.ndarray
         First vector to be expanded.

    x2 : np.ndarray
         Second vector to be expanded.

    Returns
    -------
    out : np.ndarray
          The cartesian product of combinations of the input arrays.

    Notes
    -----
    Based of original function ``gridmake2`` in CompEcon toolbox by
    Miranda and Fackler.

    References
    ----------
    Miranda, Mario J, and Paul L Fackler. Applied Computational Economics
    and Finance, MIT Press, 2002.

    """
    if x1.ndim == 1:
        if x2.ndim == 1:
            return np.column_stack([np.tile(x1, x2.shape[0]),
             np.repeat(x2, x1.shape[0])])
    if x1.ndim > 1:
        if x2.ndim == 1:
            first = np.tile(x1, (x2.shape[0], 1))
            second = np.repeat(x2, x1.shape[0])
            return np.column_stack([first, second])
    raise NotImplementedError('Come back here')