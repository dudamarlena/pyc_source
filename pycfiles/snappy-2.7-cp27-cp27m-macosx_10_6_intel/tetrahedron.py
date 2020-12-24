# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/tetrahedron.py
# Compiled at: 2017-05-26 08:27:22
from .simplex import *
import sys

class Tetrahedron:

    def __init__(self, name=''):
        self.Index = -1
        self.Name = name
        self.Neighbor = {F0: None, F1: None, F2: None, F3: None}
        self.Gluing = {F0: None, F1: None, F2: None, F3: None}
        self.Class = [None] * 16
        self.Checked = 0
        return

    def __repr__(self):
        if self.Index != -1:
            return 'tet' + str(self.Index)
        else:
            return '< floating tetrahedron ' + ' at ' + str(id(self)) + '>'

    def attach(self, two_subsimplex, tet, perm_data):
        if tet == None:
            self.Neighbor[two_subsimplex] = None
            self.Gluing[two_subsimplex] = None
        else:
            perm = Perm4(perm_data)
            self.Neighbor[two_subsimplex] = tet
            self.Gluing[two_subsimplex] = perm
            tet.Neighbor[perm.image(two_subsimplex)] = self
            tet.Gluing[perm.image(two_subsimplex)] = inv(self.Gluing[two_subsimplex])
        return

    def reverse(self):
        transpo = Perm4((1, 0, 2, 3))
        nhbr = self.Neighbor.copy()
        gluing = self.Gluing.copy()
        for two_subsimplex in TwoSubsimplices:
            relabeled = transpo.image(two_subsimplex)
            if not nhbr[two_subsimplex] == None:
                perm = (gluing[two_subsimplex] * transpo).tuple()
            else:
                perm = None
            self.attach(relabeled, nhbr[two_subsimplex], perm)

        return

    def detach(self, two_subsimplex):
        neighbor = self.Neighbor[two_subsimplex]
        if neighbor == None:
            return
        else:
            neighbors_subsimplex = self.Gluing[two_subsimplex].image(two_subsimplex)
            self.Neighbor[two_subsimplex] = None
            self.Gluing[two_subsimplex] = None
            if neighbor.Neighbor and neighbor.Neighbor[neighbors_subsimplex] == self:
                neighbor.Neighbor[neighbors_subsimplex] = None
                neighbor.Gluing[neighbors_subsimplex] = None
            return

    def erase(self):
        for two_subsimplex in TwoSubsimplices:
            self.detach(two_subsimplex)

        self.Index = -1
        self.Neighbor = None
        self.Gluing = None
        self.clear_Class()
        return

    def clear_Class(self):
        self.Class = [None] * 16
        return

    def info(self, out=sys.stdout):
        if len(self.Name) == 0:
            out.write(repr(self) + '\t%s\n' % [ self.Neighbor.get(s) for s in TwoSubsimplices ])
        else:
            out.write(repr(self) + ' ( ' + self.Name + ' )\n')
            out.write('\t%s\n' % [ self.Neighbor.get(s) for s in TwoSubsimplices ])
        out.write('\t%s\n' % [ self.Gluing.get(s) for s in TwoSubsimplices ])
        out.write('\tVertices: ' + repr(self.Class[V0]) + repr(self.Class[V1]) + repr(self.Class[V2]) + repr(self.Class[V3]) + '\n')
        if self.Index > -1:
            s = ''
            for edge in OneSubsimplices[:3]:
                s = s + '%s : %-10s   ' % (
                 SubsimplexName[edge], self.Class[edge])

            out.write('\tEdges: ' + s + '\n')
            s = ''
            for edge in OneSubsimplices[3:]:
                s = s + '%s : %-10s   ' % (
                 SubsimplexName[edge], self.Class[edge])

            out.write('\t       ' + s + '\n')

    def get_orientation_of_edge(self, a, b):
        return self.Class[(a | b)].orientation_with_respect_to(self, a, b)