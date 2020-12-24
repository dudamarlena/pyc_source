# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/graphs/layouts/random.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 1659 bytes
"""
Random Graph Layout
====================

This layout positions the nodes at random
"""
import numpy as np
from ..util import _straight_line_vertices, issparse

def random(adjacency_mat, directed=False, random_state=None):
    """
    Place the graph nodes at random places.

    Parameters
    ----------
    adjacency_mat : matrix or sparse
        The graph adjacency matrix
    directed : bool
        Whether the graph is directed. If this is True, is will also
        generate the vertices for arrows, which can be passed to an
        ArrowVisual.
    random_state : instance of RandomState | int | None
        Random state to use. Can be None to use ``np.random``.

    Yields
    ------
    (node_vertices, line_vertices, arrow_vertices) : tuple
        Yields the node and line vertices in a tuple. This layout only yields a
        single time, and has no builtin animation
    """
    if random_state is None:
        random_state = np.random
    elif not isinstance(random_state, np.random.RandomState):
        random_state = np.random.RandomState(random_state)
    if issparse(adjacency_mat):
        adjacency_mat = adjacency_mat.tocoo()
    num_nodes = adjacency_mat.shape[0]
    node_coords = random_state.rand(num_nodes, 2)
    line_vertices, arrows = _straight_line_vertices(adjacency_mat, node_coords, directed)
    yield (
     node_coords, line_vertices, arrows)