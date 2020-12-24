# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/cube.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 2537 bytes
from ..geometry import create_cube
from .mesh import MeshVisual
from .visual import CompoundVisual

class CubeVisual(CompoundVisual):
    __doc__ = 'Visual that displays a cube or cuboid\n\n    Parameters\n    ----------\n    size : float or tuple\n        The size of the cuboid. A float gives a cube, whereas tuples may\n        specify the size of each axis (x, y, z) independently.\n    vertex_colors : ndarray\n        Same as for `MeshVisual` class. See `create_cube` for vertex ordering.\n    face_colors : ndarray\n        Same as for `MeshVisual` class. See `create_cube` for vertex ordering.\n    color : Color\n        The `Color` to use when drawing the cube faces.\n    edge_color : tuple or Color\n        The `Color` to use when drawing the cube edges. If `None`, then no\n        cube edges are drawn.\n    '

    def __init__(self, size=1.0, vertex_colors=None, face_colors=None, color=(0.5, 0.5, 1, 1), edge_color=None, **kwargs):
        vertices, filled_indices, outline_indices = create_cube()
        vertices['position'] *= size
        self._mesh = MeshVisual(vertices=vertices['position'], faces=filled_indices, vertex_colors=vertex_colors, face_colors=face_colors, color=color)
        if edge_color:
            self._border = MeshVisual(vertices=vertices['position'], faces=outline_indices, color=edge_color, mode='lines')
        else:
            self._border = MeshVisual()
        CompoundVisual.__init__(self, [self._mesh, self._border], **kwargs)
        self.mesh.set_gl_state(polygon_offset_fill=True, polygon_offset=(1, 1), depth_test=True)

    @property
    def mesh(self):
        """The vispy.visuals.MeshVisual that used to fill in.
        """
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    @property
    def border(self):
        """The vispy.visuals.MeshVisual that used to draw the border.
        """
        return self._border

    @border.setter
    def border(self, border):
        self._border = border