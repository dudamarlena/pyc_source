# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/core/search.py
# Compiled at: 2019-06-30 06:40:36
# Size of source mod 2**32: 1398 bytes
import numpy as np

def find_min_neighbours(matrix: np.ndarray) -> np.ndarray:
    """Find the vertex with the minimum number of neighbouring vertices."""
    scores = np.ones(matrix.shape[0])
    for i in range(matrix.shape[0]):
        s = matrix[:, i].sum()
        scores[i] = s if s > 0 else np.inf

    return np.argmin(scores)


def eliminate_variable(idx: int, matrix: np.ndarray) -> np.ndarray:
    """Eliminate a vertex from a graph in matrix-form."""
    scope = _node_scope(idx, matrix)
    for i in scope:
        for j in scope:
            if i != j:
                matrix[(i, j)] = 1
                matrix[(j, i)] = 1

    matrix[idx, :] = 0.0
    matrix[:, idx] = 0.0
    return matrix


def _node_scope(idx: int, matrix: np.ndarray) -> np.ndarray:
    """Find the scope of given vertex."""
    return np.where(matrix[:, idx] > 0)[0]


def get_elimination_ordering(matrix: np.ndarray, heuristic: callable=find_min_neighbours):
    """Compute the elimination ordering of a given graph in matrix-from."""
    count = 0
    ordering = []
    scopes = []
    while count < matrix.shape[0] - 1:
        j = heuristic(matrix)
        scopes.append(_node_scope(j, matrix))
        matrix = eliminate_variable(j, matrix)
        ordering.append(j)
        count += 1

    ordering.append([x for x in range(matrix.shape[0]) if x not in ordering][0])
    return (
     ordering, scopes)