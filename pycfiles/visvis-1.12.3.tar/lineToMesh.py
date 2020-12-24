# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\processing\lineToMesh.py
# Compiled at: 2016-03-22 04:56:47
import numpy as np, visvis as vv
from visvis.utils.pypoints import Point, Pointset
from visvis.wobjects.polygonalModeling import BaseMesh

def getSpanVectors(normal, c, d):
    """ getSpanVectors(normal, prevA, prevB) -> (a,b)
    
    Given a normal, return two orthogonal vectors which are both orthogonal
    to the normal. The vectors are calculated so they match as much as possible
    the previous vectors.
    
    """
    a1 = d.cross(normal)
    if a1.norm() < 0.001:
        b1 = c.cross(normal)
        a1 = b1.cross(normal)
    a2 = -1 * a1
    if c.distance(a1) > c.distance(a2):
        a1 = a2
    b1 = a1.cross(normal)
    return (
     a1.normalize(), b1.normalize())


def getCircle(angles_cos, angles_sin, a, b):
    """ getCircle(angles_cos, angles_sin, a, b) -> circle_cords
    
    Creates a circle of points around the origin, 
    the circle is spanned by the vectors a and b.
    
    """
    X = np.empty((len(angles_cos), 3), dtype=np.float32)
    X[:, 0] = angles_cos * a.x + angles_sin * b.x
    X[:, 1] = angles_cos * a.y + angles_sin * b.y
    X[:, 2] = angles_cos * a.z + angles_sin * b.z
    return Pointset(X)


def lineToMesh(pp, radius, vertex_num, values=None):
    """ lineToMesh(pp, radius, vertex_num, values=None)
    
    From a line, create a mesh that represents the line as a tube with 
    given diameter. Returns a BaseMesh instance.
    
    Parameters
    ----------
    pp : 3D Pointset
        The points along the line. If the first and last point are the same,
        the mesh-line is closed.
    radius : scalar
        The radius of the tube that is created. Radius can also be a 
        sequence of values (containing a radius for each point).
    vertex_num : int
        The number of vertices to create along the circumference of the tube. 
    values : list or numpy array (optional)
        A value per point. Can be Nx1, Nx2, Nx3 or Nx4. A list of scalars
        can also be given. The values are propagated to the mesh vertices 
        and supplied as input to the Mesh constructor. This allows for example
        to define the color for the tube.
    
    """
    pi = np.pi
    if hasattr(radius, '__len__'):
        if len(radius) != len(pp):
            raise ValueError('Len of radii much match len of points.')
        else:
            radius = np.array(radius, dtype=np.float32)
    else:
        radius = radius * np.ones((len(pp),), dtype=np.float32)
    angles = np.arange(0, pi * 2 - 0.0001, pi * 2 / vertex_num)
    angle_cos = np.cos(angles)
    angle_sin = np.sin(angles)
    vertex_num2 = len(angles)
    dists = pp[1:].distance(pp[:-1])
    bufdist = min(radius.max(), dists.min() / 2.2)
    lclosed = np.all(pp[0] == pp[(-1)])
    normals = pp[:-1].subtract(pp[1:]).copy()
    if lclosed:
        normals.append(pp[0] - pp[1])
    else:
        normals.append(pp[(-2)] - pp[(-1)])
    normals = -1 * normals.normalize()
    vertices = Pointset(3)
    surfaceNormals = Pointset(3)
    if values is None:
        vvalues = None
        nvalues = 0
    else:
        if isinstance(values, list):
            if len(values) != len(pp):
                raise ValueError('There must be as many values as points.')
            vvalues = Pointset(1)
        else:
            if isinstance(values, np.ndarray):
                if values.ndim != 2:
                    raise ValueError('Values must be Nx1, Nx2, Nx3 or Nx4.')
                if values.shape[0] != len(pp):
                    raise ValueError('There must be as many values as points.')
                vvalues = Pointset(values.shape[1])
            else:
                if vv.utils.pypoints.is_Pointset(values):
                    if values.ndim > 4:
                        raise ValueError('Can specify one to four values per point.')
                    if len(values) != len(pp):
                        raise ValueError('There must be as many values as points.')
                    vvalues = Pointset(values.ndim)
                else:
                    raise ValueError('Invalid value for values.')
                n_cylinders = 0
                a, b = Point(0, 0, 1), Point(0, 1, 0)
                a, b = getSpanVectors(normals[0], a, b)
                circm = getCircle(angle_cos, angle_sin, a, b)
                if not lclosed:
                    for j in range(5, 0, -1):
                        r = (1 - (j / 5.0) ** 2) ** 0.5
                        circmp = float(r * radius[0]) * circm + (pp[0] - j / 5.0 * bufdist * normals[0])
                        circmn = pp[0].subtract(circmp).normalize()
                        vertices.extend(circmp)
                        surfaceNormals.extend(-1 * circmn)
                        if vvalues is not None:
                            for iv in range(vertex_num2):
                                vvalues.append(values[0])

                        n_cylinders += 1

                for i in range(len(pp) - 1):
                    normal1 = normals[i]
                    point1 = pp[i]
                    a, b = getSpanVectors(normal1, a, b)
                    circm = getCircle(angle_cos, angle_sin, a, b)
                    circmp = float(radius[i]) * circm + (point1 + bufdist * normal1)
                    vertices.extend(circmp)
                    surfaceNormals.extend(circm)
                    if vvalues is not None:
                        for iv in range(vertex_num2):
                            vvalues.append(values[i])

                    n_cylinders += 1
                    normal2 = normals[(i + 1)]
                    point2 = pp[(i + 1)]
                    circmp = float(radius[(i + 1)]) * circm + (point2 - bufdist * normal1)
                    vertices.extend(circmp)
                    surfaceNormals.extend(circm)
                    if vvalues is not None:
                        for iv in range(vertex_num2):
                            vvalues.append(values[(i + 1)])

                    n_cylinders += 1
                    if not lclosed and i == len(pp) - 2:
                        break
                    normal12 = (normal1 + normal2).normalize()
                    tmp = point2 + bufdist * normal2 + (point2 - bufdist * normal1)
                    point12 = 0.5858 * point2 + 0.4142 * (0.5 * tmp)
                    a, b = getSpanVectors(normal12, a, b)
                    circm = getCircle(angle_cos, angle_sin, a, b)
                    circmp = float(radius[(i + 1)]) * circm + point12
                    vertices.extend(circmp)
                    surfaceNormals.extend(circm)
                    if vvalues is not None:
                        for iv in range(vertex_num2):
                            vvalues.append(0.5 * (values[i] + values[(i + 1)]))

                    n_cylinders += 1

            if not lclosed:
                for j in range(0, 6):
                    r = (1 - (j / 5.0) ** 2) ** 0.5
                    circmp = float(r * radius[(-1)]) * circm + (pp[(-1)] + j / 5.0 * bufdist * normals[(-1)])
                    circmn = pp[(-1)].subtract(circmp).normalize()
                    vertices.extend(circmp)
                    surfaceNormals.extend(-1 * circmn)
                    if vvalues is not None:
                        for iv in range(vertex_num2):
                            vvalues.append(values[(-1)])

                    n_cylinders += 1

            else:
                normal1 = normals[(-1)]
                point1 = pp[(-1)]
                a, b = getSpanVectors(normal1, a, b)
                circm = getCircle(angle_cos, angle_sin, a, b)
                circmp = float(radius[0]) * circm + (point1 + bufdist * normal1)
                vertices.extend(circmp)
                surfaceNormals.extend(circm)
                if vvalues is not None:
                    for iv in range(vertex_num2):
                        vvalues.append(values[(-1)])

                n_cylinders += 1
            firstFace = [
             vertex_num, vertex_num + 1, 1, 0]
            lastFace = [2 * vertex_num - 1, vertex_num, 0, vertex_num - 1]
            oneRound = []
            for i in range(vertex_num - 1):
                oneRound.extend([ val + i for val in firstFace ])

        oneRound.extend(lastFace)
        oneRound = np.array(oneRound, dtype=np.uint32)
        parts = []
        for i in range(n_cylinders - 1):
            parts.append(oneRound + i * vertex_num)

    faces = np.concatenate(parts)
    faces.shape = (faces.shape[0] / 4, 4)
    return BaseMesh(vertices, faces, surfaceNormals, vvalues)