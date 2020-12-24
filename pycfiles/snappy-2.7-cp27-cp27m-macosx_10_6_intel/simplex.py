# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/simplex.py
# Compiled at: 2018-08-17 21:53:27
from .perm4 import *
SimplexError = 'Error'
N = 0
V0 = 1
V1 = 2
E01 = 3
V2 = 4
E02 = 5
E21 = 6
F3 = 7
V3 = 8
E03 = 9
E13 = 10
F2 = 11
E32 = 12
F1 = 13
F0 = 14
T = 15
E10 = 3
E20 = 5
E12 = 6
E30 = 9
E31 = 10
E23 = 12

def bitmap(tuple):
    bmap = 0
    for i in tuple:
        bmap = bmap | 1 << i

    return bmap


SubsimplexName = ('N', 'V0', 'V1', 'E01', 'V2', 'E02', 'E12', 'F3', 'V3', 'E03', 'E31',
                  'F2', 'E23', 'F1', 'F0', 'T')
Tail = {E01: V0, E02: V0, E21: V2, E03: V0, E13: V1, E32: V3}
Head = {E01: V1, E02: V2, E21: V1, E03: V3, E13: V3, E32: V2}
EdgeTuple = {E01: (0, 1), E02: (0, 2), E21: (2, 1), E03: (0, 3), E13: (1, 3), E32: (3, 2)}
RightFace = {E01: F2, E02: F3, E21: F3, E03: F1, E13: F2, E32: F1}
LeftFace = {E01: F3, E02: F1, E21: F0, E03: F2, E13: F0, E32: F0}
TopFace = {E01: F0, E02: F0, E21: F2, E03: F0, E13: F1, E32: F3}
BottomFace = {E01: F1, E02: F2, E21: F1, E03: F3, E13: F3, E32: F2}
PickAnEdge = {F0: E21, F1: E23, F2: E03, F3: E01}
OppositeEdge = {E01: E23, E02: E13, E03: E12, E12: E03, E13: E02, E23: E01}
AdjacentEdges = {E01: (E02, E03, E12, E13), E02: (
       E01, E03, E12, E23), 
   E03: (
       E01, E02, E13, E23), 
   E12: (
       E01, E02, E13, E23), 
   E13: (
       E01, E03, E12, E23), 
   E23: (
       E02, E03, E12, E13)}
TwoSubsimplices = (
 F0, F1, F2, F3)
OneSubsimplices = (
 E01, E02, E21, E03, E13, E32)
ZeroSubsimplices = (
 V0, V1, V2, V3)
FaceIndex = {F0: 0, F1: 1, F2: 2, F3: 3}
OppTail = {(V0, V1): V3, (V0, V2): V1, (V0, V3): V2, (V1, V2): V3, (V1, V3): V0, (V2, V3): V1, (V1, V0): V2, 
   (V2, V0): V3, (V3, V0): V1, (V2, V1): V0, (V3, V1): V2, (V3, V2): V0}
FacesAroundVertexCounterclockwise = {V0: (
      F1, F2, F3), 
   V1: (
      F0, F3, F2), 
   V2: (
      F0, F1, F3), 
   V3: (
      F0, F2, F1)}
VerticesOfFaceCounterclockwise = {F0: (
      V3, V2, V1), 
   F1: (
      V2, V3, V0), 
   F2: (
      V3, V1, V0), 
   F3: (
      V1, V2, V0)}

def is_subset(x, y):
    if x & y == x:
        return 1
    return 0


def comp(subsimplex):
    return ~subsimplex & 15


def flip_face(edge, face):
    return edge | ~face & 15