# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\processing\calculateNormals.py
# Compiled at: 2016-03-22 05:01:25
# Size of source mod 2**32: 5038 bytes
import numpy as np, time
v = np.array([10, 11, 12, 20, 21, 22, 30, 31, 32, 40, 41, 42, 50, 51, 52, 60, 61, 62])
v.shape = (6, 3)
N = v.shape[0]
faces = np.arange(N)
faces.shape = (
 len(v) // 3, 3)

def calculateNormals(mesh):
    """ calculateNormals(mesh)
    
    Calculate the normal data from the vertices.
    Handles triangular and quad faces.
    
    """
    t0 = time.time()
    vertices = mesh._vertices
    if vertices is None:
        return
    N = vertices.shape[0]
    normals = np.zeros((N, 3), dtype='float32')
    faces = mesh._GetFaces()
    Nfaces, vpf = faces.shape
    Nfaces = faces.size / vpf
    if vpf == 3:
        v1 = vertices[faces[:, 0]]
        v2 = vertices[faces[:, 1]]
        v3 = vertices[faces[:, 2]]
        _vectorsToNormals(v2 - v1, v2 - v3, faces, normals)
    elif vpf == 4:
        v1 = vertices[faces[:, 0]]
        v2 = vertices[faces[:, 1]]
        v3 = vertices[faces[:, 2]]
        v4 = vertices[faces[:, 3]]
        _vectorsToNormals(v2 - v1, v2 - v3, faces, normals)
        _vectorsToNormals(v2 - v4, v2 - v3, faces, normals)
        _vectorsToNormals(v1 - v3, v4 - v3, faces, normals)
        _vectorsToNormals(v2 - v1, v1 - v4, faces, normals)
    lengths = normals[:, 0] ** 2 + normals[:, 1] ** 2 + normals[:, 2] ** 2
    lengths = lengths ** 0.5
    normals[:, 0] /= lengths
    normals[:, 1] /= lengths
    normals[:, 2] /= lengths
    I, = np.where(lengths == 0)
    normals[(I, 0)] = 0
    normals[(I, 1)] = 0
    normals[(I, 2)] = 1
    mesh._normals = -normals


def _vectorsToNormals(a, b, faces, normals):
    normalsPerFace = np.zeros((faces.shape[0], 3), dtype='float32')
    normalsPerFace[:, 0] = a[:, 1] * b[:, 2] - a[:, 2] * b[:, 1]
    normalsPerFace[:, 1] = a[:, 2] * b[:, 0] - a[:, 0] * b[:, 2]
    normalsPerFace[:, 2] = a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]
    Nfaces = faces.shape[0]
    if Nfaces > 32000:
        for f in range(faces.shape[1]):
            normals[faces[:, f]] += normalsPerFace

    else:
        for f in range(faces.shape[1]):
            for i in range(faces.shape[0]):
                normals[faces[(i, f)]] += normalsPerFace[i]


def calculateNormals_old(mesh):
    """ calculateNormals(mesh)
    
    Calculate the normal data from the vertices.
    Handles triangular and quad faces.
    
    """
    t0 = time.time()
    vertices = mesh._vertices
    if vertices is None:
        return
    N = vertices.shape[0]
    normals = np.zeros((N, 3), dtype='float32')
    defaultNormal = np.array([1, 0, 0], dtype='float32')
    for ii in mesh._IterFaces():
        v1 = vertices[ii[0], :]
        v2 = vertices[ii[1], :]
        v3 = vertices[ii[2], :]
        tmp = np.cross(v1 - v2, v2 - v3)
        if np.isnan(tmp).sum():
            tmp = defaultNormal
        normals[ii[0], :] += tmp
        normals[ii[1], :] += tmp
        normals[ii[2], :] += tmp

    for i in range(N):
        tmp = normals[i, :]
        tmp = tmp / (tmp ** 2).sum() ** 0.5
        if np.isnan(tmp).sum():
            tmp = defaultNormal
        normals[i, :] = -tmp

    print('calculated normals in %1.2 s' % (time.time() - t0))
    mesh._normals = normals