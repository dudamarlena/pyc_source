# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/objloader.py
# Compiled at: 2018-05-08 07:23:32
# Size of source mod 2**32: 6308 bytes
from typing import List, Union
from pathlib import Path
import numpy as np

class ObjLoader:

    def __init__(self, objFile: Union[(Path, str)]):
        self.geomVert = []
        self.normVert = []
        self.texVert = []
        self.smoothingGroups = {'__DEFAULT__': []}
        self.verts = None
        if issubclass(type(objFile), Path):
            self.readFile(objFile)
        else:
            if type(objFile) is str:
                self.readFile(Path(objFile))

    def readFile(self, path: Path):
        """Open Obj file, read and parse each line"""
        currentSmoothingGroup = '__DEFAULT__'
        with path.open('r') as (f):
            for line in f:
                if line.startswith('v '):
                    self.geomVert.append(self.parseVertCoords(line))
                elif line.startswith('vn '):
                    self.normVert.append(self.parseVertCoords(line))
                elif line.startswith('vt '):
                    self.texVert.append(self.parseVertCoords(line))
                elif line.startswith('f '):
                    face = self.parseFace(line)
                    if len(face) > 3:
                        face = self.triangulateConvexFace(face)
                        self.smoothingGroups[currentSmoothingGroup] += face
                    else:
                        self.smoothingGroups[currentSmoothingGroup] += [face]
                elif line.startswith('s '):
                    sarg = line[2:].rstrip('\n').rstrip('\r')
                    if sarg == 'off':
                        currentSmoothingGroup = '__DEFAULT__'
                    else:
                        currentSmoothingGroup = sarg
                if currentSmoothingGroup not in self.smoothingGroups:
                    self.smoothingGroups[currentSmoothingGroup] = []

        verts = []
        for group in self.smoothingGroups:
            if self.smoothingGroups[group]:
                verts.append(self.processSmoothingGroup(self.smoothingGroups[group]))

        self.verts = verts

    def processSmoothingGroup(self, group, maxangle=70) -> List[float]:
        """Process smoothing groups to vertices
        Two modes:
        1.) Face is defined with normals. No further processing needed, just emit three vertices per face.
        2.) Face is defined without normals. In this case: calculate face normals + face normals of all adjacent faces.
            If vertex is shared by multiple faces, average face normals if their angle is smaller than maxangle.

        Mode is determined by probing the first face."""
        vertexData = []
        if group[0][0][2] is not None:
            mode = 1
        else:
            mode = 2
        for face in group:
            if mode == 1:
                for vertIndices in face:
                    vertexData += self.geomVert[vertIndices[0]]
                    vertexData += self.texVert[vertIndices[1]][0:2]
                    vertexData += self.normVert[vertIndices[2]]

            if mode == 2:
                vert1 = self.geomVert[face[0][0]]
                vert2 = self.geomVert[face[1][0]]
                vert3 = self.geomVert[face[2][0]]
                edge1 = np.array(vert2, np.float32) - np.array(vert1, np.float32)
                edge2 = np.array(vert3, np.float32) - np.array(vert2, np.float32)
                calcnorm = np.cross(edge1, edge2)
                calcnorm /= np.linalg.norm(calcnorm)
                for vertIndices in face:
                    vertexData += self.geomVert[vertIndices[0]]
                    vertexData += self.texVert[vertIndices[1]][0:2]
                    vertexData += [calcnorm[0], calcnorm[1], calcnorm[2]]

        return vertexData

    @staticmethod
    def parseVertCoords(line):
        """Read a vertex line and parse the coordinates
        Format of line: 'K coord0 coord1 coord2 [...]"""
        return [float(x) for x in line.split(' ')[1:]]

    @staticmethod
    def parseFace(line) -> List[List[int]]:
        """Read a face line and parse the vertex indices
        Each face can be described in fundamentally two different ways:
          1: list of indices of geometry vertices
            ex: 'f v0 v1 v2 [...]'
          2: list of tuples of indices of geometry vertices, texture vertices and normal vertices (optional)
            ex: 'f v0/vt0/vn0 v1/vt1/vn1 v2/vt2/vn2 [...]'
            ex: 'f v0//vn0 v1//vn1 v2//vn2 [...]'
            ex: 'f v0/vt0 v1/vt1 v2/vt2 [...]'
        All indices are 1-based, so we need to deduct one on parsing.
        """
        faceIndices = []
        for faceTuple in [x for x in line.split(' ')[1:]]:
            parsedTuple = []
            for index in [x for x in faceTuple.split('/')]:
                try:
                    index = int(index) - 1
                except ValueError:
                    raise
                    index = None

                parsedTuple.append(index)

            while len(parsedTuple) < 3:
                parsedTuple.append(None)

            faceIndices.append(parsedTuple)

        return faceIndices

    @staticmethod
    def triangulateConvexFace(face: List[List[int]]) -> List[List[int]]:
        """Triangulate a convex face into triangles using a fan
        Assumes CCW order of vertices"""
        newfaces = []
        start = face[0]
        helper = face[1]
        for i in range(2, len(face)):
            newfaces.append([start, helper, face[i]])
            helper = face[i]

        return newfaces