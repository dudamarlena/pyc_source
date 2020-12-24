# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/game_theory/vertex_enumeration.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 11233 bytes
"""
Compute all mixed Nash equilibria of a 2-player normal form game by
vertex enumeration.

References
----------
B. von Stengel, "Equilibrium Computation for Two-Player Games in
Strategic and Extensive Form," Chapter 3, N. Nisan, T. Roughgarden, E.
Tardos, and V. Vazirani eds., Algorithmic Game Theory, 2007.

"""
import numpy as np, scipy.spatial
from numba import jit, guvectorize

def vertex_enumeration(g, qhull_options=None):
    """
    Compute mixed-action Nash equilibria of a 2-player normal form game
    by enumeration and matching of vertices of the best response
    polytopes. For a non-degenerate game input, these are all the Nash
    equilibria.

    Internally, `scipy.spatial.ConvexHull` is used to compute vertex
    enumeration of the best response polytopes, or equivalently, facet
    enumeration of their polar polytopes. Then, for each vertex of the
    polytope for player 0, vertices of the polytope for player 1 are
    searched to find a completely labeled pair.

    Parameters
    ----------
    g : NormalFormGame
        NormalFormGame instance with 2 players.

    qhull_options : str, optional(default=None)
        Options to pass to `scipy.spatial.ConvexHull`. See the `Qhull
        manual <http://www.qhull.org>`_  for details.

    Returns
    -------
    list(tuple(ndarray(float, ndim=1)))
        List containing tuples of Nash equilibrium mixed actions.

    """
    return list(vertex_enumeration_gen(g, qhull_options=qhull_options))


def vertex_enumeration_gen(g, qhull_options=None):
    """
    Generator version of `vertex_enumeration`.

    Parameters
    ----------
    g : NormalFormGame
        NormalFormGame instance with 2 players.

    qhull_options : str, optional(default=None)
        Options to pass to `scipy.spatial.ConvexHull`. See the `Qhull
        manual <http://www.qhull.org>`_  for details.

    Yields
    -------
    tuple(ndarray(float, ndim=1))
        Tuple of Nash equilibrium mixed actions.

    """
    try:
        N = g.N
    except AttributeError:
        raise TypeError('input must be a 2-player NormalFormGame')

    if N != 2:
        raise NotImplementedError('Implemented only for 2-player games')
    brps = [_BestResponsePolytope((g.players[(1 - i)]), idx=i, qhull_options=qhull_options) for i in range(N)]
    labelings_bits_tup = tuple((_ints_arr_to_bits(brps[i].labelings) for i in range(N)))
    equations_tup = tuple((brps[i].equations for i in range(N)))
    trans_recips = tuple((brps[i].trans_recip for i in range(N)))
    return _vertex_enumeration_gen(labelings_bits_tup, equations_tup, trans_recips)


@jit(nopython=True)
def _vertex_enumeration_gen(labelings_bits_tup, equations_tup, trans_recips):
    """
    Main body of `vertex_enumeration_gen`.

    Parameters
    ----------
    labelings_bits_tup : tuple(ndarray(np.uint64, ndim=1))
        Tuple of ndarrays of integers representing labelings of the
        vertices of the best response polytopes.

    equations_tup : tuple(ndarray(float, ndim=2))
        Tuple of ndarrays containing the hyperplane equations of the
        polar polytopes.

    trans_recips : tuple(scalar(float))
        Tuple of the reciprocals of the translations.

    """
    m, n = equations_tup[0].shape[1] - 1, equations_tup[1].shape[1] - 1
    num_vertices0, num_vertices1 = equations_tup[0].shape[0], equations_tup[1].shape[0]
    ZERO_LABELING0_BITS = (np.uint64(1) << np.uint64(m)) - np.uint64(1)
    COMPLETE_LABELING_BITS = (np.uint64(1) << np.uint64(m + n)) - np.uint64(1)
    for i in range(num_vertices0):
        if labelings_bits_tup[0][i] == ZERO_LABELING0_BITS:
            continue
        for j in range(num_vertices1):
            xor = labelings_bits_tup[0][i] ^ labelings_bits_tup[1][j]
            if xor == COMPLETE_LABELING_BITS:
                yield _get_mixed_actions(labelings_bits_tup[0][i], (
                 equations_tup[0][i], equations_tup[1][j]), trans_recips)
                break


class _BestResponsePolytope:
    __doc__ = '\n    Class that represents a best response polytope for a player in a\n    two-player normal form game.\n\n    Let :math:`A` and :math:`B` be the m x n and n x m payoff matrices\n    of players 0 and 1, respectively, where the payoffs are assumed to\n    have been shifted in such a way that :math:`A` and :math:`B` are\n    nonnegative and have no zero column. In von Stegel (2007), the best\n    response polytope for player 0 is defined by\n\n    .. math::\n\n        P = \\{x \\in \\mathbb{R}^m \\mid x \\geq 0,\\ B x \\leq 1\\},\n\n    and that for player 1 by\n\n    .. math::\n\n        Q = \\{y \\in \\mathbb{R}^n \\mid A y \\leq 1,\\ y \\geq 0\\}.\n\n    Here, by translation we represent these in the form\n\n    .. math::\n\n        \\hat{P} = \\{z \\in \\mathbb{R}^m \\mid D z \\leq 1\\},\n\n    and\n\n    .. math::\n\n        \\hat{Q} = \\{w \\in \\mathbb{R}^n \\mid C w \\leq 1\\},\n\n    where :math:`D` and :math:`C` are (m+n) x m and (m+n) x n matrices,\n    respectively. The 2d array of matrix :math:`D` for player 0 (or\n    :math:`C` for player 1) is passed as its `points` argument to\n    `scipy.spatial.ConvexHull`, which then computes, by the Qhull\n    library, convex hull (or facet enumeration). By polar duality, this\n    is equivalent to vertex enumeration of the polytope :math:`\\hat{P}`,\n    where its k-th vertex is obtained by `-equations[k, :-1]/\n    equations[k, -1]`, and the indices of the corresponding binding\n    inequalities by `labelings[k]`, while the vertex of the original\n    polytope :math:`P` can be obtained by `-equations[k, :-1]/\n    equations[k, -1] + 1/trans_recip`.\n\n    Parameters\n    ----------\n    opponent_player : Player\n        Instance of Player with one opponent.\n\n    idx : scalar(int), optional(default=0)\n        Player index in the normal form game, either 0 or 1.\n\n    qhull_options : str, optional(default=None)\n        Options to pass to `scipy.spatial.ConvexHull`. See the `Qhull\n        manual <http://www.qhull.org>`_  for details.\n\n    Attributes\n    ----------\n    ndim : scalar(int)\n        Dimension of the polytope.\n\n    hull : scipy.spatial.ConvexHull\n        `ConvexHull` instance reprensenting the polar polytope.\n\n    num_vertices : scalar(int)\n        Number of the vertices identified by `ConvexHull`.\n\n    equations : ndarray(float, ndim=2)\n        Output of `ConvexHull.equations`. The k-th vertex is obtained\n        by `-equations[k, :-1]/equations[k, -1]`.\n\n    labelings : ndarray(int32, ndim=2)\n        Output of `ConvexHull.simplices`. `labelings[k]` stores the\n        indices of the binding inequalities for the k-th vertex.\n\n    trans_recip : scalar(float)\n        Reciprocal of the translation; the k-th vertex of the original\n        polytope before translation can be computed by\n        `-equations[k, :-1]/equations[k, -1] + 1/trans_recip`.\n\n    '

    def __init__(self, opponent_player, idx=0, qhull_options=None):
        try:
            num_opponents = opponent_player.num_opponents
        except AttributeError:
            raise TypeError('input must be a Player instance')

        if num_opponents != 1:
            raise NotImplementedError('Implemented only for Player in a 2-player game')
        B = opponent_player.payoff_array
        n, m = B.shape
        self.ndim = m
        D = np.empty((m + n, m))
        nonneg_cond_start, payoff_cond_start = (0, m) if idx == 0 else (n, 0)
        col_mins = B.min(axis=0)
        col_maxs = B.max(axis=0)
        nonpos_const_cols = (col_maxs == col_mins) * (col_mins <= 0)
        shifts = np.zeros(m)
        shifts[col_mins < 0] = -col_mins[(col_mins < 0)]
        shifts[nonpos_const_cols] += 1
        D[payoff_cond_start:payoff_cond_start + n, :] = B + shifts
        row_sums = D[payoff_cond_start:payoff_cond_start + n, :].sum(axis=1)
        trans_recip = row_sums.max() * 2
        D[payoff_cond_start:payoff_cond_start + n, :] *= trans_recip
        D[payoff_cond_start:payoff_cond_start + n, :] /= (trans_recip - row_sums).reshape(n, 1)
        D[nonneg_cond_start:nonneg_cond_start + m, :] = 0
        np.fill_diagonal(D[nonneg_cond_start:nonneg_cond_start + m, :], -trans_recip)
        self.hull = scipy.spatial.ConvexHull(D, qhull_options=qhull_options)
        self.equations = self.hull.equations
        self.labelings = self.hull.simplices
        self.num_vertices = self.hull.equations.shape[0]
        self.trans_recip = trans_recip


@guvectorize(['(i4[:], u8[:])'], '(m)->()', nopython=True, cache=True)
def _ints_arr_to_bits(ints_arr, out):
    """
    Convert an array of integers representing the set bits into the
    corresponding integer.

    Compiled as a ufunc by Numba's `@guvectorize`: if the input is a
    2-dim array with shape[0]=K, the function returns a 1-dim array of
    K converted integers.

    Parameters
    ----------
    ints_arr : ndarray(int32, ndim=1)
        Array of distinct integers from 0, ..., 63.

    Returns
    -------
    np.uint64
        Integer with set bits represented by the input integers.

    Examples
    --------
    >>> ints_arr = np.array([0, 1, 2], dtype=np.int32)
    >>> _ints_arr_to_bits(ints_arr)
    7
    >>> ints_arr2d = np.array([[0, 1, 2], [3, 0, 1]], dtype=np.int32)
    >>> _ints_arr_to_bits(ints_arr2d)
    array([ 7, 11], dtype=uint64)

    """
    m = ints_arr.shape[0]
    out[0] = 0
    for i in range(m):
        out[0] |= np.uint64(1) << np.uint64(ints_arr[i])


@jit(nopython=True, cache=True)
def _get_mixed_actions(labeling_bits, equation_tup, trans_recips):
    """
    From a labeling for player 0, a tuple of hyperplane equations of the
    polar polytopes, and a tuple of the reciprocals of the translations,
    return a tuple of the corresponding, normalized mixed actions.

    Parameters
    ----------
    labeling_bits : scalar(np.uint64)
        Integer with set bits representing a labeling of a mixed action
        of player 0.

    equation_tup : tuple(ndarray(float, ndim=1))
        Tuple of hyperplane equations of the polar polytopes.

    trans_recips : tuple(scalar(float))
        Tuple of the reciprocals of the translations.

    Returns
    -------
    tuple(ndarray(float, ndim=1))
        Tuple of mixed actions.

    """
    m, n = equation_tup[0].shape[0] - 1, equation_tup[1].shape[0] - 1
    out = np.empty(m + n)
    for pl, (start, stop, skip) in enumerate([(0, m, np.uint64(1)),
     (
      m, m + n, np.uint64(0))]):
        sum_ = 0.0
        for i in range(start, stop):
            if labeling_bits & np.uint64(1) == skip:
                out[i] = 0
            else:
                out[i] = equation_tup[pl][(i - start)] * trans_recips[pl] - equation_tup[pl][(-1)]
                sum_ += out[i]
            labeling_bits = labeling_bits >> np.uint64(1)

        if sum_ != 0:
            out[start:stop] /= sum_

    return (
     out[:m], out[m:])