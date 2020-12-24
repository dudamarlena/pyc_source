# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/graphs/layouts/circular.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 1514 bytes
"""
Circular Layout
===============

This module contains several graph layouts which rely heavily on circles.
"""
import numpy as np
from ..util import _straight_line_vertices, issparse

def circular(adjacency_mat, directed=False):
    """Places all nodes on a single circle.

    Parameters
    ----------
    adjacency_mat : matrix or sparse
        The graph adjacency matrix
    directed : bool
        Whether the graph is directed. If this is True, is will also
        generate the vertices for arrows, which can be passed to an
        ArrowVisual.

    Yields
    ------
    (node_vertices, line_vertices, arrow_vertices) : tuple
        Yields the node and line vertices in a tuple. This layout only yields a
        single time, and has no builtin animation
    """
    if issparse(adjacency_mat):
        adjacency_mat = adjacency_mat.tocoo()
    num_nodes = adjacency_mat.shape[0]
    t = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False, dtype=np.float32)
    node_coords = (0.5 * np.array([np.cos(t), np.sin(t)]) + 0.5).T
    line_vertices, arrows = _straight_line_vertices(adjacency_mat, node_coords, directed)
    yield (
     node_coords, line_vertices, arrows)