# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/util.py
# Compiled at: 2018-11-28 16:08:20
# Size of source mod 2**32: 2819 bytes
from typing import Union, List, Tuple
from pathlib import Path
from OpenGL import GL
import numpy as np
from typing import NamedTuple

def ObjLoader(objFilePath: Path):
    vertices = []
    uv = []
    normals = []
    faces = []
    normsavailable = False
    with objFilePath.open('r') as (f):
        for line in f:
            lineSplit = line.split(' ')
            if line.startswith('vt'):
                uv.append([float(lineSplit[1]), float(lineSplit[2])])
            elif line.startswith('vn'):
                normals.append([float(lineSplit[1]), float(lineSplit[2]), float(lineSplit[3])])
                normsavailable = True
            elif line.startswith('v'):
                vertices.append([float(lineSplit[1]), float(lineSplit[2]), float(lineSplit[3])])
            elif line.startswith('f'):
                faces.append([[int(x) - 1 for x in lineSplit[1].split('/')],
                 [int(x) - 1 for x in lineSplit[2].split('/')],
                 [int(x) - 1 for x in lineSplit[3].split('/')]])

    outdata = np.array([], np.float32)
    for face in faces:
        if not normsavailable:
            edge1 = np.array(vertices[face[1][0]], np.float32) - np.array(vertices[face[0][0]], np.float32)
            edge2 = np.array(vertices[face[2][0]], np.float32) - np.array(vertices[face[1][0]], np.float32)
            calcnorm = np.cross(edge1, edge2)
            calcnorm /= np.linalg.norm(calcnorm)
        for vert in face:
            v = vertices[vert[0]]
            uvval = uv[vert[1]]
            if normsavailable:
                n = normals[vert[2]]
                outdata = np.append(outdata, np.array(v + uvval + n, np.float32))
            else:
                outdata = np.append(outdata, np.array(v + uvval, np.float32))
                outdata = np.append(outdata, calcnorm)

    texturedata = None
    return (
     outdata, texturedata)


def Vec2(v0: Union[(int, float)]=0, v1: Union[(int, float)]=0):
    return np.array([v0, v1], np.float32)


def Vec3(v0: Union[(int, float)]=0, v1: Union[(int, float)]=0, v2: Union[(int, float)]=0):
    return np.array([v0, v1, v2], np.float32)


def Vec4(v0: Union[(int, float)]=0, v1: Union[(int, float)]=0, v2: Union[(int, float)]=0, v3: Union[(int, float)]=0):
    return np.array([v0, v1, v2, v3], np.float32)


class Resolution(NamedTuple):
    width = 800
    width: int
    height = 600
    height: int