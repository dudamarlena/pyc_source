# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/arrow.py
# Compiled at: 2017-05-26 08:27:22
from .simplex import *
from .tetrahedron import *

class Arrow:

    def __init__(self, edge, face, tet):
        self.Edge = edge
        self.Face = face
        self.Tetrahedron = tet

    def __repr__(self):
        return '< ' + SubsimplexName[self.Edge] + ' | ' + SubsimplexName[self.Face] + ' | ' + str(self.Tetrahedron) + ' >'

    def head(self):
        return self.Face & comp(self.Edge)

    def tail(self):
        return comp(self.Face)

    def equator(self):
        return self.Tetrahedron.Class[comp(self.Edge)]

    def axis(self):
        return self.Tetrahedron.Class[self.Edge]

    def north_head(self):
        return self.Tetrahedron.Class[(self.head() | OppTail[(self.head(), self.tail())])]

    def south_head(self):
        return self.Tetrahedron.Class[(self.head() | OppTail[(self.tail(), self.head())])]

    def north_tail(self):
        return self.Tetrahedron.Class[(self.tail() | OppTail[(self.head(), self.tail())])]

    def south_tail(self):
        return self.Tetrahedron.Class[(self.tail() | OppTail[(self.tail(), self.head())])]

    def is_null(self):
        if self.Tetrahedron is None:
            return 1
        else:
            return 0

    def reverse(self):
        self.Face = flip_face(self.Edge, self.Face)
        return self

    def next(self):
        if not self.Tetrahedron == None:
            perm = self.Tetrahedron.Gluing[self.Face]
            tet = self.Tetrahedron.Neighbor[self.Face]
        if tet == None:
            return
        else:
            self.Edge = perm.image(self.Edge)
            self.Face = flip_face(self.Edge, perm.image(self.Face))
            self.Tetrahedron = tet
            return self

    def glue(self, other):
        if self.Tetrahedron == None and other.Tetrahedron == None:
            return
        else:
            if self.Tetrahedron == None:
                other.reverse().glue(self)
                other.reverse()
                return
            if other.Tetrahedron == None:
                self.Tetrahedron.attach(self.Face, None, (0, 1, 2, 3))
                return
            self.Tetrahedron.attach(self.Face, other.Tetrahedron, {FaceIndex[self.Face]: FaceIndex[flip_face(other.Edge, other.Face)], FaceIndex[flip_face(self.Edge, self.Face)]: FaceIndex[other.Face]})
            return

    def glued(self):
        a = self.copy()
        if a.next() == None:
            a.Tetrahedron = None
        return a

    def opposite(self):
        self.Face = comp(OppTail[(self.tail(), self.head())])
        self.Edge = comp(self.Edge)
        return self

    def rotate(self, n):
        for i in range(n % 3):
            head = self.head()
            tail = self.tail()
            self.Edge = tail | OppTail[(tail, head)]
            self.Face = self.Edge | head

        return self

    def copy(self):
        return Arrow(self.Edge, self.Face, self.Tetrahedron)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            if self.Tetrahedron == None and other.Tetrahedron == None:
                return True
            if self.Tetrahedron == other.Tetrahedron and self.Edge == other.Edge and self.Face == other.Face:
                return True
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def linking_cycle(self):
        a = self.copy()
        cycle = []
        while 1:
            cycle.append(a.Tetrahedron.Class[OppositeEdge[a.Edge]])
            a.next()
            if a == self:
                break

        return cycle

    def radii(self):
        a = self.copy()
        radius_list = []
        while 1:
            a.rotate(2)
            radius_list.append(a.Tetrahedron.Class[OppositeEdge[a.Edge]])
            a.rotate(1).next()
            if a == self:
                break

        return radius_list


class eArrow(Arrow):

    def __init__(self, tet, tail, head):
        self.Edge = comp(tail | head)
        self.Face = comp(tail)
        self.Tetrahedron = tet