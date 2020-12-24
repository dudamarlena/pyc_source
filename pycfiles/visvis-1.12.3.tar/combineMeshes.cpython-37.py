# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\processing\combineMeshes.py
# Compiled at: 2017-05-31 20:05:28
# Size of source mod 2**32: 1951 bytes
import numpy as np
from visvis.wobjects.polygonalModeling import BaseMesh

def combineMeshes(meshes):
    """ combineMeshes(meshes)
    
    Given a list of mesh objects, produces a combined mesh.
    
    """
    if not meshes:
        raise ValueError('No meshes or empty meshes given')
    vpf = 0
    hasNormals = True
    hasFaces = True
    hasValues = True
    for mesh in meshes:
        if vpf == 0:
            hasFaces = mesh._faces is not None
            vpf = mesh._verticesPerFace
        else:
            if mesh._verticesPerFace != vpf:
                raise ValueError('Cannot combine meshes with different verticesPerFace.')
            if (mesh._faces is not None) != hasFaces:
                raise ValueError('Cannot combine meshes with and without face data.')
        hasNormals = hasNormals and mesh._normals is not None
        hasValues = hasValues and mesh._values is not None

    vertices = np.concatenate([m._vertices for m in meshes])
    faces = None
    if hasFaces:
        facesList = []
        startIndex = 0
        for mesh in meshes:
            facesList.append(mesh._faces + startIndex)
            startIndex += mesh._vertices.shape[0]

        faces = np.concatenate(facesList)
    normals = None
    if hasNormals:
        normals = np.concatenate([m._normals for m in meshes])
    values = None
    if hasValues:
        values = np.concatenate([m._values for m in meshes])
    return BaseMesh(vertices, faces, normals, values, vpf)