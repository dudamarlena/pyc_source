# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\processing\unwindFaces.py
# Compiled at: 2016-03-22 04:56:47
# Size of source mod 2**32: 1729 bytes
import numpy as np

def unwindFaces(mesh):
    """ unwindFaces(mesh)
    
    Unwinds the faces to make new versions of the vertices, normals,
    values, which are usually larger. The new arrays 
    represent the same surface, but is described without a faces
    array. 
    
    """
    if mesh._faces is None:
        return
    faces = mesh._faces
    N = faces.shape[0]
    if mesh._vertices is not None:
        vertices = mesh._vertices
        newVertices = np.zeros((N, 3), dtype='float32')
        for i in range(N):
            newVertices[i, :] = vertices[faces[i]]

        mesh._vertices = newVertices
    if mesh._normals is not None:
        normals = mesh._normals
        newNormals = np.zeros((N, 3), dtype='float32')
        for i in range(N):
            newNormals[i, :] = normals[faces[i]]

        mesh._normals = newNormals
        mesh._flatNormals = None
    if mesh._values is not None:
        values = mesh._values
        M = values.shape[1]
        newValues = np.zeros((N, M), dtype='float32')
        for i in range(N):
            newValues[i, :] = values[faces[i]]

        mesh._values = newValues
    mesh._faces = None