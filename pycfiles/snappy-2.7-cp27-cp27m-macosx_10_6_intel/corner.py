# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/corner.py
# Compiled at: 2017-05-26 08:27:22
from .simplex import *
from .tetrahedron import *

class Corner:

    def __init__(self, tetrahedron, subsimplex):
        self.Tetrahedron = tetrahedron
        self.Subsimplex = subsimplex

    def __repr__(self):
        return '<' + SubsimplexName[self.Subsimplex] + ' of ' + str(self.Tetrahedron) + '>'