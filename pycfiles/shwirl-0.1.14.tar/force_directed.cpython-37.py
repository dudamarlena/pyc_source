# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/graphs/layouts/force_directed.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 7486 bytes
"""
Force-Directed Graph Layout
===========================

This module contains implementations for a force-directed layout, where the
graph is modelled like a collection of springs or as a collection of
particles attracting and repelling each other. The whole graph tries to
reach a state which requires the minimum energy.
"""
import numpy as np
try:
    from scipy.sparse import issparse
except ImportError:

    def issparse(*args, **kwargs):
        return False


from ..util import _straight_line_vertices, _rescale_layout

class fruchterman_reingold(object):
    __doc__ = '\n    Fruchterman-Reingold implementation adapted from NetworkX.\n\n    In the Fruchterman-Reingold algorithm, the whole graph is modelled as a\n    collection of particles, it runs a simplified particle simulation to\n    find a nice layout for the graph.\n\n    Paramters\n    ---------\n    optimal : number\n        Optimal distance between nodes. Defaults to :math:`1/\\sqrt{N}` where\n        N is the number of nodes.\n    iterations : int\n        Number of iterations to perform for layout calculation.\n    pos : array\n        Initial positions of the nodes\n\n    Notes\n    -----\n    The algorithm is explained in more detail in the original paper [1]_.\n\n    .. [1] Fruchterman, Thomas MJ, and Edward M. Reingold. "Graph drawing by\n       force-directed placement." Softw., Pract. Exper. 21.11 (1991),\n       1129-1164.\n    '

    def __init__(self, optimal=None, iterations=50, pos=None):
        self.dim = 2
        self.optimal = optimal
        self.iterations = iterations
        self.num_nodes = None
        self.pos = pos

    def __call__(self, adjacency_mat, directed=False):
        """
        Starts the calculation of the graph layout.

        This is a generator, and after each iteration it yields the new
        positions for the nodes, together with the vertices for the edges
        and the arrows.

        There are two solvers here: one specially adapted for SciPy sparse
        matrices, and the other for larger networks.

        Parameters
        ----------
        adjacency_mat : array
            The graph adjacency matrix.
        directed : bool
            Wether the graph is directed or not. If this is True,
            it will draw arrows for directed edges.

        Yields
        ------
        layout : tuple
            For each iteration of the layout calculation it yields a tuple
            containing (node_vertices, line_vertices, arrow_vertices). These
            vertices can be passed to the `MarkersVisual` and `ArrowVisual`.
        """
        if adjacency_mat.shape[0] != adjacency_mat.shape[1]:
            raise ValueError('Adjacency matrix should be square.')
        else:
            self.num_nodes = adjacency_mat.shape[0]
            if issparse(adjacency_mat):
                solver = self._sparse_fruchterman_reingold
            else:
                solver = self._fruchterman_reingold
        for result in solver(adjacency_mat, directed):
            yield result

    def _fruchterman_reingold(self, adjacency_mat, directed=False):
        if self.optimal is None:
            self.optimal = 1 / np.sqrt(self.num_nodes)
        elif self.pos is None:
            pos = np.asarray((np.random.random((self.num_nodes, self.dim))),
              dtype=(np.float32))
        else:
            pos = self.pos.astype(np.float32)
        line_vertices, arrows = _straight_line_vertices(adjacency_mat, pos, directed)
        yield (pos, line_vertices, arrows)
        t = 0.1
        dt = t / float(self.iterations + 1)
        for iteration in range(self.iterations):
            delta_pos = _calculate_delta_pos(adjacency_mat, pos, t, self.optimal)
            pos += delta_pos
            _rescale_layout(pos)
            t -= dt
            line_vertices, arrows = _straight_line_vertices(adjacency_mat, pos, directed)
            yield (
             pos, line_vertices, arrows)

    def _sparse_fruchterman_reingold(self, adjacency_mat, directed=False):
        if self.optimal is None:
            self.optimal = 1 / np.sqrt(self.num_nodes)
        else:
            adjacency_arr = adjacency_mat.toarray()
            adjacency_coo = adjacency_mat.tocoo()
            if self.pos is None:
                pos = np.asarray((np.random.random((self.num_nodes, self.dim))),
                  dtype=(np.float32))
            else:
                pos = self.pos.astype(np.float32)
        line_vertices, arrows = _straight_line_vertices(adjacency_coo, pos, directed)
        yield (pos, line_vertices, arrows)
        t = 0.1
        dt = t / float(self.iterations + 1)
        for iteration in range(self.iterations):
            delta_pos = _calculate_delta_pos(adjacency_arr, pos, t, self.optimal)
            pos += delta_pos
            _rescale_layout(pos)
            t -= dt
            line_vertices, arrows = _straight_line_vertices(adjacency_coo, pos, directed)
            yield (
             pos, line_vertices, arrows)


def _calculate_delta_pos(adjacency_arr, pos, t, optimal):
    """Helper to calculate the delta position"""
    delta = pos[:, np.newaxis, :] - pos
    distance2 = (delta * delta).sum(axis=(-1))
    distance2 = np.where(distance2 < 0.0001, 0.0001, distance2)
    distance = np.sqrt(distance2)
    displacement = np.zeros((len(delta), 2))
    for ii in range(2):
        displacement[:, ii] = (delta[:, :, ii] * (optimal * optimal / (distance * distance) - adjacency_arr * distance / optimal)).sum(axis=1)

    length = np.sqrt((displacement ** 2).sum(axis=1))
    length = np.where(length < 0.01, 0.1, length)
    delta_pos = displacement * t / length[:, np.newaxis]
    return delta_pos