# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\staticrab\correlation.py
# Compiled at: 2020-04-25 11:14:47
# Size of source mod 2**32: 934 bytes
import staticrab_backend as B, numpy as np

def chatterjee(x: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the Chatterjee's correlation measure.

    The function computes the Chatterjee's correlation measure.

    Parameters
    ----------
    x:
        array of float64
    y:
        array of float64, cannot be constant

    Examples
    --------

    >>> a = np.array(range(5), dtype=np.float64)
    >>> chatterjee(a, a)
    0.5
    """
    if len(np.unique(y)) == 1:
        raise ValueError('The y cannot be constant.')
    if x.dtype != np.float64:
        raise ValueError(f"Only the dtype = np.float64 is supported. The provided x has dtype {x.dtype}.")
    if y.dtype != np.float64:
        raise ValueError(f"Only the dtype = np.float64 is supported. The provided y has dtype {y.dtype}.")
    return B.chatterjee(x, y, False)