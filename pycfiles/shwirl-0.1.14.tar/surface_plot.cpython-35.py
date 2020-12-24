# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/surface_plot.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 5503 bytes
from __future__ import division
import numpy as np
from .mesh import MeshVisual
from ..geometry import MeshData

class SurfacePlotVisual(MeshVisual):
    __doc__ = 'Displays a surface plot on a regular x,y grid\n\n    Parameters\n    ----------\n    x : ndarray | None\n        1D array of values specifying the x positions of vertices in the\n        grid. If None, values will be assumed to be integers.\n    y : ndarray | None\n        1D array of values specifying the x positions of vertices in the\n        grid. If None, values will be assumed to be integers.\n    z : ndarray\n        2D array of height values for each grid vertex.\n    colors : ndarray\n        (width, height, 4) array of vertex colors.\n\n    Notes\n    -----\n    All arguments are optional.\n\n    Note that if vertex positions are updated, the normal vectors for each\n    triangle must be recomputed. This is somewhat expensive if the surface\n    was initialized with smooth=False and very expensive if smooth=True.\n    For faster performance, initialize with compute_normals=False and use\n    per-vertex colors or a material that does not require normals.\n    '

    def __init__(self, x=None, y=None, z=None, colors=None, **kwargs):
        self._x = None
        self._y = None
        self._z = None
        self._SurfacePlotVisual__vertices = None
        self._SurfacePlotVisual__faces = None
        self._SurfacePlotVisual__meshdata = MeshData()
        kwargs.setdefault('shading', 'smooth')
        MeshVisual.__init__(self, **kwargs)
        self.set_data(x, y, z, colors)

    def set_data(self, x=None, y=None, z=None, colors=None):
        """Update the data in this surface plot.

        Parameters
        ----------
        x : ndarray | None
            1D array of values specifying the x positions of vertices in the
            grid. If None, values will be assumed to be integers.
        y : ndarray | None
            1D array of values specifying the x positions of vertices in the
            grid. If None, values will be assumed to be integers.
        z : ndarray
            2D array of height values for each grid vertex.
        colors : ndarray
            (width, height, 4) array of vertex colors.
        """
        if x is not None:
            if self._x is None or len(x) != len(self._x):
                self._SurfacePlotVisual__vertices = None
            self._x = x
        if y is not None:
            if self._y is None or len(y) != len(self._y):
                self._SurfacePlotVisual__vertices = None
            self._y = y
        if z is not None:
            if self._x is not None and z.shape[0] != len(self._x):
                raise TypeError('Z values must have shape (len(x), len(y))')
            if self._y is not None and z.shape[1] != len(self._y):
                raise TypeError('Z values must have shape (len(x), len(y))')
            self._z = z
            if self._SurfacePlotVisual__vertices is not None and self._z.shape != self._SurfacePlotVisual__vertices.shape[:2]:
                self._SurfacePlotVisual__vertices = None
        if self._z is None:
            return
        update_mesh = False
        new_vertices = False
        if self._SurfacePlotVisual__vertices is None:
            new_vertices = True
            self._SurfacePlotVisual__vertices = np.empty((self._z.shape[0], self._z.shape[1], 3), dtype=np.float32)
            self.generate_faces()
            self._SurfacePlotVisual__meshdata.set_faces(self._SurfacePlotVisual__faces)
            update_mesh = True
        if new_vertices or x is not None:
            if x is None:
                if self._x is None:
                    x = np.arange(self._z.shape[0])
                else:
                    x = self._x
                self._SurfacePlotVisual__vertices[:, :, 0] = x.reshape(len(x), 1)
                update_mesh = True
        if new_vertices or y is not None:
            if y is None:
                if self._y is None:
                    y = np.arange(self._z.shape[1])
                else:
                    y = self._y
                self._SurfacePlotVisual__vertices[:, :, 1] = y.reshape(1, len(y))
                update_mesh = True
        if new_vertices or z is not None:
            self._SurfacePlotVisual__vertices[(Ellipsis, 2)] = self._z
            update_mesh = True
        if colors is not None:
            self._SurfacePlotVisual__meshdata.set_vertex_colors(colors)
            update_mesh = True
        if update_mesh:
            self._SurfacePlotVisual__meshdata.set_vertices(self._SurfacePlotVisual__vertices.reshape(self._SurfacePlotVisual__vertices.shape[0] * self._SurfacePlotVisual__vertices.shape[1], 3))
            MeshVisual.set_data(self, meshdata=self._SurfacePlotVisual__meshdata)

    def generate_faces(self):
        cols = self._z.shape[1] - 1
        rows = self._z.shape[0] - 1
        faces = np.empty((cols * rows * 2, 3), dtype=np.uint)
        rowtemplate1 = np.arange(cols).reshape(cols, 1) + np.array([[0, 1, cols + 1]])
        rowtemplate2 = np.arange(cols).reshape(cols, 1) + np.array([[cols + 1, 1, cols + 2]])
        for row in range(rows):
            start = row * cols * 2
            faces[start:start + cols] = rowtemplate1 + row * (cols + 1)
            faces[start + cols:start + cols * 2] = rowtemplate2 + row * (cols + 1)

        self._SurfacePlotVisual__faces = faces