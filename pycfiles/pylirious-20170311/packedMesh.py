# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\shared\tim_working\development\github\pylirious\pylirious\mm-api\python\mm\packedMesh.py
# Compiled at: 2016-07-24 13:10:59
from mm.mm_math import *
import struct

class packedMesh(object):
    """
    This class represents a packed mesh
    """

    def __init__(self):
        """initialize empty mesh"""
        self.vertices = []
        self.triangles = []
        self.normals = []
        self.colors = []

    def appendVertex(self, pos, normal=(), color=()):
        vID = len(self.vertices)
        self.vertices.append(pos)
        if len(normal) > 0:
            self.normals.append(normal)
        if len(color) > 0:
            self.colors.append(color)
        return vID

    def appendTriangle(self, tri):
        tID = len(self.triangles)
        self.triangles.append(tri)
        return tID

    def writeOBJ(self, path):
        with open(path, 'w') as (f):
            for v in self.vertices:
                f.write('v %f %f %f\n' % v)

            for t in self.triangles:
                t2 = tuple(addvs(t, 1))
                f.write('f %d %d  %d ' % t2)

        f.close()

    def write(self, path):
        with open(path, 'wb') as (f):
            have_colors = False
            if len(self.colors) > 0:
                have_colors = True
            have_normals = False
            if len(self.normals) == len(self.vertices):
                have_normals = True
            version = 1
            f.write(struct.pack('i', version))
            f.write(struct.pack('i', len(self.vertices)))
            vertex_flags = 0
            if have_normals:
                vertex_flags = vertex_flags | 4
            if have_colors:
                vertex_flags = vertex_flags | 8
            f.write(struct.pack('i', vertex_flags))
            for v in self.vertices:
                f.write(struct.pack('f', v[0]))
                f.write(struct.pack('f', v[1]))
                f.write(struct.pack('f', v[2]))

            if have_normals:
                for n in self.normals:
                    f.write(struct.pack('f', n[0]))
                    f.write(struct.pack('f', n[1]))
                    f.write(struct.pack('f', n[2]))

            if have_colors:
                for c in self.colors:
                    f.write(struct.pack('f', c[0]))
                    f.write(struct.pack('f', c[1]))
                    f.write(struct.pack('f', c[2]))

            f.write(struct.pack('i', len(self.triangles)))
            f.write(struct.pack('i', 0))
            for t in self.triangles:
                f.write(struct.pack('i', t[0]))
                f.write(struct.pack('i', t[1]))
                f.write(struct.pack('i', t[2]))

        f.close()