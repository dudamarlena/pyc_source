# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/operations/marginalise.py
# Compiled at: 2019-06-15 16:42:10
# Size of source mod 2**32: 1686 bytes
import numpy as np, apogee as ap

def factor_marginalise(a, v):
    """
    Marginalise out the variable 'v' from factor 'a'.

    Parameters
    ----------
    a: Factor-like
        The target factor-like object.
    v: int/any
        The identifier of the variable to be marginalised out.

    Returns
    -------
    scope: ndarray
        An array containing the scope of the resulting factor.
    card: ndarray
        An array containing the cardinality of the resulting factor.
    vals: ndarray
        An array containing the probability distribution of the resulting factor.

    Examples
    --------
    >>> a = Factor([0], [2], [0.1, 0.9])
    >>> b = Factor([1, 0], [2, 2], [[0.2, 0.8], [0.7, 0.3]])
    >>> c = Factor(*factor_marginalise(a, 0))  # generate new factor from factors a and b
        {0: {0: 0.5, 1: 0.5}, 1: {0: 0.25, 1: 0.75}}

    """
    scope = a.scope[np.where(a.scope != v)]
    f_map = ap.index_map_1d(a.scope, scope)
    card = a.cards[f_map]
    assignments = (ap.cartesian_product)(*[np.arange(x) for x in card])
    f_idx = ap.array_index(a.assignments[:, f_map], assignments)
    values = np.zeros((len(assignments)), dtype=(np.float64))
    avals = a.parameters
    for i in range(len(a.assignments)):
        if values[f_idx[i]] is None:
            values[f_idx[i]] = avals[i]
        else:
            values[f_idx[i]] += avals[i]

    return (scope, card, values)