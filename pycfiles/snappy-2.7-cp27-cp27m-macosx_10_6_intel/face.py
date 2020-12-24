# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/face.py
# Compiled at: 2017-05-26 08:27:22
from .arrow import *
from .simplex import *
from .tetrahedron import *
from .corner import *

class Face:

    def __init__(self):
        self.Index = -1
        self.IntOrBdry = ''
        self.Corners = []

    def __repr__(self):
        if self.Index > -1:
            return 'f' + str(self.Index) + ' (' + self.IntOrBdry + ')'
        else:
            return '< floating face' + str(id(self)) + ' >'

    def erase(self):
        for corner in self.Corners:
            corner.Tetrahedron.Class[corner.Subsimplex] = None

        self.Index = -1
        return

    def bdry_arrow(self):
        if self.IntOrBdry != 'bdry':
            return None
        else:
            face = self.Corners[0].Subsimplex
            tet = self.Corners[0].Tetrahedron
            edge = PickAnEdge[face]
            return Arrow(edge, face, tet)