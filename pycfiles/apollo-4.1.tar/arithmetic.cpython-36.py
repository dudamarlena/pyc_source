# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/operations/arithmetic.py
# Compiled at: 2019-06-15 16:47:32
# Size of source mod 2**32: 1010 bytes
from typing import Tuple, Callable
import numpy as np, apogee as ap

def factor_arithmetic(a: Tuple[(np.ndarray, np.ndarray, np.ndarray, np.ndarray)], b: Tuple[(np.ndarray, np.ndarray, np.ndarray, np.ndarray)], op: Callable) -> Tuple[(np.ndarray, np.ndarray, np.ndarray)]:
    scope = ap.union1d(a[0], b[0])
    maps_a = ap.array_mapping(scope, a[0])
    maps_b = ap.array_mapping(scope, b[0])
    card = np.zeros_like(scope, dtype=(np.int32))
    card[maps_a] = a[1]
    card[maps_b] = b[1]
    assignments = (ap.cartesian_product)(*[np.arange(n, dtype=(np.int32)) for n in card])
    vals = np.empty((len(assignments)), dtype=(type(a[2][0])))
    a_idx = ap.array_index(assignments[:, maps_a], a[3])
    b_idx = ap.array_index(assignments[:, maps_b], b[3])
    a_vals, b_vals = a[2], b[2]
    for i, (j, k) in enumerate(zip(a_idx, b_idx)):
        vals[i] = op(a_vals[j], b_vals[k])

    return (
     scope, card, vals)