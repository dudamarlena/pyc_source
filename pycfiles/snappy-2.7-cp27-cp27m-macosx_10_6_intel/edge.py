# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/edge.py
# Compiled at: 2018-08-17 21:53:27
from .simplex import *
from .tetrahedron import *
from .corner import *
from .arrow import *
from .perm4 import *
import sys

class Edge:

    def __init__(self):
        self.Index = -1
        self.Name = ''
        self.IntOrBdry = ''
        self.Corners = []
        self.Vertices = []
        self.LeftBdryArrow = None
        self.RightBdryArrow = None
        self._edge_orient_cache = dict()
        return

    def __repr__(self):
        if self.Index > -1:
            return 'e' + str(self.Index) + self.Name + ' (' + self.IntOrBdry + ')'
        else:
            return '< floating edge' + str(id(self)) + ' >'

    def get_arrow(self):
        e = self.Corners[0].Subsimplex
        return Arrow(e, RightFace[e], self.Corners[0].Tetrahedron)

    def info(self, out=sys.stdout):
        out.write(repr(self) + '\t Edge of valence %d\tEndpoints %s\n' % (
         self.valence(), self.Vertices))
        if self.IntOrBdry == 'bdry':
            a = self.LeftBdryArrow.copy()
            a.reverse()
        else:
            a = self.get_arrow()
        s = '\t'
        for i in range(self.valence()):
            s = s + repr(a) + '  '
            a.next()
            if i > 0 and (i + 1) % 3 == 0 and i != self.valence() - 1:
                s = s + '\n\t'

        out.write(s + '\n')

    def valence(self):
        return len(self.Corners)

    def distinct(self):
        for corner in self.Corners:
            corner.Tetrahedron.Checked = 0

        for corner in self.Corners:
            if corner.Tetrahedron.Checked == 1:
                return 0
            corner.Tetrahedron.Checked = 1

        return 1

    def self_adjacent(self):
        for corner in self.Corners:
            for one_subsimplex in AdjacentEdges[corner.Subsimplex]:
                if corner.Tetrahedron.Class[one_subsimplex] is self:
                    return 1

        return 0

    def self_opposite(self):
        count = 0
        for corner in self.Corners:
            if corner.Tetrahedron.Class[comp(corner.Subsimplex)] == self:
                count = count + 1

        return count / 2

    def erase(self):
        for corner in self.Corners:
            corner.Tetrahedron.Class[corner.Subsimplex] = None

        for vertex in self.Vertices:
            try:
                vertex.Edges.remove(self)
            except:
                pass

        self.Index = -1
        return

    def orientation_with_respect_to(self, tet, a, b):
        try:
            return self._edge_orient_cache[(tet, a, b)]
        except IndexError:
            raise ValueError('Given corner of tet not on this edge')

    def index(self):
        return self.Index

    def _first_embedding(self):
        """
      For this edge, return an edge embedding similar
      to regina, that is a pair (tetrahedron, permutation) such that
      vertex 0 and 1 of the tetrahedron span the edge.
      """
        corner = self.Corners[0]
        tet = corner.Tetrahedron
        for perm in Perm4.A4():
            if corner.Subsimplex == perm.image(E01):
                if tet.Class[perm.image(V0)] == self.Vertices[0]:
                    if tet.Class[perm.image(V1)] == self.Vertices[1]:
                        return (tet, perm)

    def embeddings(self):
        """
      Iterator through the embeddings of this edge.
      An edge embedding is a pair (tetrahedron, permutation) such that
      vertices of the tetrahedron that are labeled by the images of 0 and 1
      under the permutation span the edge. The images of 2 and 3 of the edge
      embeddings are in an orientation compatible way.
      This is similar to the NEdgeEmbeddings of regina.
      """
        order = len(self.Corners)
        tet, perm = self._first_embedding()
        for i in range(order):
            yield (
             tet, perm)
            face = perm.image(11)
            tet, perm = tet.Neighbor[face], tet.Gluing[face] * perm * Perm4((0, 1,
                                                                             3, 2))

    def _add_corner(self, arrow):
        """
      Used by Mcomplex.build_edge_classes
      """
        self.Corners.append(Corner(arrow.Tetrahedron, arrow.Edge))
        other_arrow = arrow.copy().opposite()
        tail, head = other_arrow.tail(), other_arrow.head()
        self._edge_orient_cache[(arrow.Tetrahedron, tail, head)] = 1
        self._edge_orient_cache[(arrow.Tetrahedron, head, tail)] = -1