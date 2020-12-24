# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/tube.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 5524 bytes
from __future__ import division
from .mesh import MeshVisual
import numpy as np
from numpy.linalg import norm
from ..util.transforms import rotate
from ..color import ColorArray

class TubeVisual(MeshVisual):
    __doc__ = "Displays a tube around a piecewise-linear path.\n\n    The tube mesh is corrected following its Frenet curvature and\n    torsion such that it varies smoothly along the curve, including if\n    the tube is closed.\n\n    Parameters\n    ----------\n    points : ndarray\n        An array of (x, y, z) points describing the path along which the\n        tube will be extruded.\n    radius : float\n        The radius of the tube. Defaults to 1.0.\n    closed : bool\n        Whether the tube should be closed, joining the last point to the\n        first. Defaults to False.\n    color : Color | ColorArray\n        The color(s) to use when drawing the tube. The same color is\n        applied to each vertex of the mesh surrounding each point of\n        the line. If the input is a ColorArray, the argument will be\n        cycled; for instance if 'red' is passed then the entire tube\n        will be red, or if ['green', 'blue'] is passed then the points\n        will alternate between these colours. Defaults to 'purple'.\n    tube_points : int\n        The number of points in the circle-approximating polygon of the\n        tube's cross section. Defaults to 8.\n    shading : str | None\n        Same as for the `MeshVisual` class. Defaults to 'smooth'.\n    vertex_colors: ndarray | None\n        Same as for the `MeshVisual` class.\n    face_colors: ndarray | None\n        Same as for the `MeshVisual` class.\n    mode : str\n        Same as for the `MeshVisual` class. Defaults to 'triangles'.\n\n    "

    def __init__(self, points, radius=1.0, closed=False, color='purple', tube_points=8, shading='smooth', vertex_colors=None, face_colors=None, mode='triangles'):
        points = np.array(points)
        tangents, normals, binormals = _frenet_frames(points, closed)
        segments = len(points) - 1
        grid = np.zeros((len(points), tube_points, 3))
        for i in range(len(points)):
            pos = points[i]
            normal = normals[i]
            binormal = binormals[i]
            v = np.arange(tube_points, dtype=np.float) / tube_points * 2 * np.pi
            cx = -1.0 * radius * np.cos(v)
            cy = radius * np.sin(v)
            grid[i] = pos + cx[:, np.newaxis] * normal + cy[:, np.newaxis] * binormal

        indices = []
        for i in range(segments):
            for j in range(tube_points):
                ip = (i + 1) % segments if closed else i + 1
                jp = (j + 1) % tube_points
                index_a = i * tube_points + j
                index_b = ip * tube_points + j
                index_c = ip * tube_points + jp
                index_d = i * tube_points + jp
                indices.append([index_a, index_b, index_d])
                indices.append([index_b, index_c, index_d])

        vertices = grid.reshape(grid.shape[0] * grid.shape[1], 3)
        color = ColorArray(color)
        if vertex_colors is None:
            point_colors = np.resize(color.rgba, (
             len(points), 4))
            vertex_colors = np.repeat(point_colors, tube_points, axis=0)
        indices = np.array(indices, dtype=np.uint32)
        MeshVisual.__init__(self, vertices, indices, vertex_colors=vertex_colors, face_colors=face_colors, shading=shading, mode=mode)


def _frenet_frames(points, closed):
    """Calculates and returns the tangents, normals and binormals for
    the tube."""
    tangents = np.zeros((len(points), 3))
    normals = np.zeros((len(points), 3))
    epsilon = 0.0001
    tangents = np.roll(points, -1, axis=0) - np.roll(points, 1, axis=0)
    if not closed:
        tangents[0] = points[1] - points[0]
        tangents[-1] = points[(-1)] - points[(-2)]
    mags = np.sqrt(np.sum(tangents * tangents, axis=1))
    tangents /= mags[:, np.newaxis]
    t = np.abs(tangents[0])
    smallest = np.argmin(t)
    normal = np.zeros(3)
    normal[smallest] = 1.0
    vec = np.cross(tangents[0], normal)
    normals[0] = np.cross(tangents[0], vec)
    for i in range(1, len(points)):
        normals[i] = normals[(i - 1)]
        vec = np.cross(tangents[(i - 1)], tangents[i])
        if norm(vec) > epsilon:
            vec /= norm(vec)
            theta = np.arccos(np.clip(tangents[(i - 1)].dot(tangents[i]), -1, 1))
            normals[i] = rotate(-np.degrees(theta), vec)[:3, :3].dot(normals[i])

    if closed:
        theta = np.arccos(np.clip(normals[0].dot(normals[(-1)]), -1, 1))
        theta /= len(points) - 1
        if tangents[0].dot(np.cross(normals[0], normals[(-1)])) > 0:
            theta *= -1.0
        for i in range(1, len(points)):
            normals[i] = rotate(-np.degrees(theta * i), tangents[i])[:3, :3].dot(normals[i])

    binormals = np.cross(tangents, normals)
    return (
     tangents, normals, binormals)