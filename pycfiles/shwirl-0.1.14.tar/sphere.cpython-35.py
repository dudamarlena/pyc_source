# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/sphere.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 3002 bytes
from ..geometry import create_sphere
from .mesh import MeshVisual
from .visual import CompoundVisual

class SphereVisual(CompoundVisual):
    __doc__ = "Visual that displays a sphere\n\n    Parameters\n    ----------\n    radius : float\n        The size of the sphere.\n    cols : int\n        Number of cols that make up the sphere mesh\n        (for method='latitude' and 'cube').\n    rows : int\n        Number of rows that make up the sphere mesh\n        (for method='latitude' and 'cube').\n    depth : int\n        Number of depth segments that make up the sphere mesh\n        (for method='cube').\n    subdivisions : int\n        Number of subdivisions to perform (for method='ico').\n    method : str\n        Method for generating sphere. Accepts 'latitude' for\n        latitude-longitude, 'ico' for icosahedron, and 'cube'\n        for cube based tessellation.\n    vertex_colors : ndarray\n        Same as for `MeshVisual` class.\n        See `create_sphere` for vertex ordering.\n    face_colors : ndarray\n        Same as for `MeshVisual` class.\n        See `create_sphere` for vertex ordering.\n    color : Color\n        The `Color` to use when drawing the sphere faces.\n    edge_color : tuple or Color\n        The `Color` to use when drawing the sphere edges. If `None`, then no\n        sphere edges are drawn.\n    "

    def __init__(self, radius=1.0, cols=30, rows=30, depth=30, subdivisions=3, method='latitude', vertex_colors=None, face_colors=None, color=(0.5, 0.5, 1, 1), edge_color=None, **kwargs):
        mesh = create_sphere(cols, rows, depth, radius=radius, subdivisions=subdivisions, method=method)
        self._mesh = MeshVisual(vertices=mesh.get_vertices(), faces=mesh.get_faces(), vertex_colors=vertex_colors, face_colors=face_colors, color=color)
        if edge_color:
            self._border = MeshVisual(vertices=mesh.get_vertices(), faces=mesh.get_edges(), color=edge_color, mode='lines')
        else:
            self._border = MeshVisual()
        CompoundVisual.__init__(self, [self._mesh, self._border], **kwargs)
        self.mesh.set_gl_state(polygon_offset_fill=True, polygon_offset=(1, 1), depth_test=True)

    @property
    def mesh(self):
        """The vispy.visuals.MeshVisual that used to fil in.
        """
        return self._mesh

    @property
    def border(self):
        """The vispy.visuals.MeshVisual that used to draw the border.
        """
        return self._border