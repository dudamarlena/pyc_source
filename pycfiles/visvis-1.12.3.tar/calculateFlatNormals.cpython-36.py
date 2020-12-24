# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\processing\calculateFlatNormals.py
# Compiled at: 2017-05-31 20:05:28
# Size of source mod 2**32: 1722 bytes
import numpy as np
from visvis.processing.unwindFaces import unwindFaces

def calculateFlatNormals(mesh):
    """ calculateFlatNormals(mesh)
    
    Calculate a variant of the normals that is more suited for
    flat shading. This is done by setting the first normal for each
    face (the one used when flat shading is used) to the average
    of all normals of that face. This can in some cases lead to
    wrong results if a vertex is the first vertex of more than one
    face.
    
    """
    unwindFaces(mesh)
    normals = mesh._normals
    if normals is None:
        return
    N = normals.shape[0]
    flatNormals = np.zeros((N, 3), dtype='float32')
    faces = mesh._GetFaces()
    vpf = mesh._verticesPerFace
    for i in range(vpf):
        I = faces[:, i]
        for j in range(vpf):
            J = faces[:, j]
            flatNormals[J] += normals[I]

    flatNormals /= vpf
    mesh._flatNormals = flatNormals