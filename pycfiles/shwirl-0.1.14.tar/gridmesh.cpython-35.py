# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/gridmesh.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 3347 bytes
from .mesh import MeshVisual
from ..geometry import create_grid_mesh, MeshData

class GridMeshVisual(MeshVisual):
    __doc__ = "Displays a mesh in a Cartesian grid about x,y,z coordinates.\n\n    This makes it simple to generate a mesh from e.g. the output\n    of numpy.meshgrid.\n\n    All arguments are optional, though they can be changed\n    individually later with the set_data method.\n\n    Parameters\n    ----------\n    xs : ndarray\n        A 2d array of x coordinates for the vertices of the mesh. Must\n        have the same dimensions as ys and zs.\n    ys : ndarray\n        A 2d array of y coordinates for the vertices of the mesh. Must\n        have the same dimensions as xs and zs.\n    zs : ndarray\n        A 2d array of z coordinates for the vertices of the mesh. Must\n        have the same dimensions as xs and ys.\n    colors : ndarray | None\n        The colors of the points of the mesh. Should be either a\n        (width, height, 4) array of rgba colors at each grid point or\n        a (width, height, 3) array of rgb colors at each grid point.\n        Defaults to None, in which case the default color of a\n        MeshVisual is used.\n    shading : str | None\n        Same as for the `MeshVisual` class. Defaults to 'smooth'.\n    **kwargs :\n        Other arguments are passed directly to MeshVisual.\n    "

    def __init__(self, xs, ys, zs, colors=None, shading='smooth', **kwargs):
        if xs is None or ys is None or zs is None:
            raise ValueError('All of xs, ys and zs must be initialised with arrays.')
        self._xs = None
        self._ys = None
        self._zs = None
        self._GridMeshVisual__vertices = None
        self._GridMeshVisual__meshdata = MeshData()
        MeshVisual.__init__(self, shading=shading, **kwargs)
        self.set_data(xs, ys, zs, colors)

    def set_data(self, xs=None, ys=None, zs=None, colors=None):
        """Update the mesh data.

        Parameters
        ----------
        xs : ndarray | None
            A 2d array of x coordinates for the vertices of the mesh.
        ys : ndarray | None
            A 2d array of y coordinates for the vertices of the mesh.
        zs : ndarray | None
            A 2d array of z coordinates for the vertices of the mesh.
        colors : ndarray | None
            The color at each point of the mesh. Must have shape
            (width, height, 4) or (width, height, 3) for rgba or rgb
            color definitions respectively.
        """
        if xs is None:
            xs = self._xs
            self._GridMeshVisual__vertices = None
        if ys is None:
            ys = self._ys
            self._GridMeshVisual__vertices = None
        if zs is None:
            zs = self._zs
            self._GridMeshVisual__vertices = None
        if self._GridMeshVisual__vertices is None:
            vertices, indices = create_grid_mesh(xs, ys, zs)
            self._xs = xs
            self._ys = ys
            self._zs = zs
        if self._GridMeshVisual__vertices is None:
            vertices, indices = create_grid_mesh(self._xs, self._ys, self._zs)
            self._GridMeshVisual__meshdata.set_vertices(vertices)
            self._GridMeshVisual__meshdata.set_faces(indices)
        if colors is not None:
            self._GridMeshVisual__meshdata.set_vertex_colors(colors.reshape(colors.shape[0] * colors.shape[1], colors.shape[2]))
        MeshVisual.set_data(self, meshdata=self._GridMeshVisual__meshdata)