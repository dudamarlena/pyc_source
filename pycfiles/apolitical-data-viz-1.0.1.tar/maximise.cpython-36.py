# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/operations/maximise.py
# Compiled at: 2019-06-15 16:42:10
# Size of source mod 2**32: 772 bytes
import numpy as np, apogee as ap
from .utils import index_to_assignment, assignment_to_index

def factor_maximise(a, v):
    scope = a.scope[np.where(a.scope != v)]
    f_map = ap.index_map_1d(a.scope, scope)
    card = a.cards[f_map]
    assignments = (ap.cartesian_product)(*[np.arange(n) for n in card])
    values = np.ones((len(assignments)), dtype=(np.float64)) * -np.inf
    avals = a.params
    for i in range(len(a.params)):
        j = assignment_to_index(index_to_assignment(i, a.cards)[f_map], card)
        values[j] = np.max([values[j], avals[i]])

    return (
     scope, card, values)