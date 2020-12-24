# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/files.py
# Compiled at: 2019-07-15 23:56:54
from __future__ import unicode_literals
from .arrow import eArrow
from .simplex import *
from .tetrahedron import Tetrahedron
import os, sys, re

def read_SnapPea_file(file_name=None, data=None):
    if data is None:
        data = open(file_name).read().decode(b'ascii')
    count = 0
    neighbors_match = b'^\\s*(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s*$'
    perm_match = b'\\s*([0123]{4,4})\\s+([0123]{4,4})\\s+([0123]{4,4})\\s+([0123]{4,4})\\s*$'
    snappea_re = re.compile(neighbors_match + perm_match, re.MULTILINE)
    fake_tets = []
    curr_poss = 0
    while 1:
        m = snappea_re.search(data, curr_poss)
        if not m:
            break
        else:
            neighbors = [ int(g) for g in m.group(1, 2, 3, 4) ]
            perms = []
            for perm in m.group(5, 6, 7, 8):
                perm = [ int(p) for p in [perm[0], perm[1], perm[2], perm[3]] ]
                perms.append(perm)

            fake_tets.append((neighbors, perms))
            curr_poss = m.end(8)

    return fake_tets


def write_SnapPea_file(mcomplex, fileobject):
    out = fileobject.write
    if hasattr(fileobject, b'name'):
        name = fileobject.name
    else:
        name = b'untitled'
    out(b'% Triangulation\n\n' + name + b'\nnot_attempted 0.0\nunknown_orientability\nCS_unknown\n\n')
    torus_cusps = []
    for vertex in mcomplex.Vertices:
        g = vertex.link_genus()
        if g > 1:
            raise ValueError(b'Link of vertex has genus more than 1.')
        if g == 1:
            torus_cusps.append(vertex)

    out(b'%d 0\n' % len(torus_cusps))
    for i in torus_cusps:
        out(b'   torus   0.000000000000   0.000000000000\n')

    out(b'\n')
    out(b'%d\n' % len(mcomplex))
    for tet in mcomplex.Tetrahedra:
        for face in TwoSubsimplices:
            out(b'    %d' % mcomplex.Tetrahedra.index(tet.Neighbor[face]))

        out(b'\n')
        for face in TwoSubsimplices:
            out(b' %d%d%d%d' % tet.Gluing[face].tuple())

        out(b'\n')
        for vert in ZeroSubsimplices:
            vertex = tet.Class[vert]
            if vertex.link_genus() == 1:
                out(b'%d ' % torus_cusps.index(vertex))
            else:
                out(b'-1 ')

        out(b'\n')
        for i in range(4):
            out(b'0 0 0 0  0 0 0 0   0 0 0 0   0 0 0 0\n')

        out(b'0.0 0.0\n\n')


conv = {b'u': V0, b'v': V1, b'w': V2, b'x': V3}
conv_back = {V0: b'u', V1: b'v', V2: b'w', V3: b'x'}

def read_edge(edge):
    m = re.match(b'([0-9]+)([uvwx])([uvwx])', edge)
    return (int(m.group(1)) - 1, conv[m.group(2)], conv[m.group(3)])


def read_geo_file(file_name, num_tet=None):
    data = open(file_name).readlines()
    if num_tet == None:
        num_tet = len(data) - 2
    tets = []
    for i in range(num_tet):
        tets.append(Tetrahedron())

    for line in data[1:]:
        line = line.decode(b'ascii')
        cycle = re.split(b'\\s+', line[:-1])[1:]
        for i in range(len(cycle)):
            t1, v1, v2 = read_edge(cycle[i])
            t2, w1, w2 = read_edge(cycle[((i + 1) % len(cycle))])
            a = eArrow(tets[t1], v1, v2)
            b = eArrow(tets[t2], w1, w2)
            a.glue(b)

    return Mcomplex(tets)


def write_geo_file(mcomplex, fileobject):
    out = fileobject.write
    out(b'k\n')
    i = 1
    for edge in mcomplex.Edges:
        tet = edge.Corners[0].Tetrahedron
        edge_name = edge.Corners[0].Subsimplex
        init = Head[edge_name]
        fin = Tail[edge_name]
        a = eArrow(tet, init, fin).opposite()
        b = a.copy()
        out(b'%d\t%d%s%s ' % (i, mcomplex.Tetrahedra.index(b.Tetrahedron) + 1,
         conv_back[b.tail()], conv_back[b.head()]))
        b.next()
        while b != a:
            out(b'%d%s%s ' % (mcomplex.Tetrahedra.index(b.Tetrahedron) + 1,
             conv_back[b.tail()], conv_back[b.head()]))
            b.next()

        i = i + 1
        out(b'\n')


def write_spine_file(mcomplex, fileobject):
    out = fileobject.write
    for edge in mcomplex.Edges:
        n = edge.valence()
        A = edge.get_arrow()
        tets, global_faces, local_faces, back_local_faces = ([], [], [], [])
        for i in range(n):
            tets.append(A.Tetrahedron.Index + 1)
            global_faces.append(A.Tetrahedron.Class[A.Face].Index + 1)
            local_faces.append(A.Face)
            back_local_faces.append(comp(A.head()))
            A.next()

        signs = [ 1 if (tets[i], local_faces[i]) < (tets[((i + 1) % n)], back_local_faces[((i + 1) % n)]) else -1 for i in range(n) ]
        ans = repr([ signs[i] * global_faces[i] for i in range(n) ])[1:-1].replace(b',', b'')
        out(ans + b'\n')


__all__ = ('read_SnapPea_file', 'write_SnapPea_file', 'read_geo_file', 'write_geo_file',
           'write_spine_file')