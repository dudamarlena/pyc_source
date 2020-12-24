# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/vertex.py
# Compiled at: 2017-05-26 08:27:22
from .simplex import *
from .tetrahedron import *
from .corner import *
from .edge import *

class Vertex:

    def __init__(self):
        self.Index = -1
        self.IntOrBdry = ''
        self.Corners = []
        self.Edges = []

    def __repr__(self):
        if self.Index > -1:
            return 'v' + str(self.Index) + ' (' + self.IntOrBdry + ') '
        else:
            return '< floating vertex' + str(id(self)) + ' >'

    def erase(self):
        for corner in self.Corners:
            corner.Tetrahedron.Class[corner.Subsimplex] = None

        for edge in self.Edges:
            try:
                edge.Vertices.remove(self)
            except:
                pass

        self.Index = -1
        return

    def link_genus(self):
        sum = 12
        for edge in self.Edges:
            sum = sum - 6 + edge.valence()

        return sum / 12