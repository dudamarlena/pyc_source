# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/plane.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 2209 bytes
from ..geometry import create_plane
from .visual import CompoundVisual
from .mesh import MeshVisual

class PlaneVisual(CompoundVisual):
    __doc__ = "Visual that displays a plane.\n\n    Parameters\n    ----------\n    width : float\n        Plane width.\n    height : float\n        Plane height.\n    width_segments : int\n        Plane segments count along the width.\n    height_segments : float\n        Plane segments count along the height.\n    direction: unicode\n        ``{'-x', '+x', '-y', '+y', '-z', '+z'}``\n        Direction the plane will be facing.\n    vertex_colors : ndarray\n        Same as for `MeshVisual` class. See `create_plane` for vertex ordering.\n    face_colors : ndarray\n        Same as for `MeshVisual` class. See `create_plane` for vertex ordering.\n    color : Color\n        The `Color` to use when drawing the cube faces.\n    edge_color : tuple or Color\n        The `Color` to use when drawing the cube edges. If `None`, then no\n        cube edges are drawn.\n    "

    def __init__(self, width=1, height=1, width_segments=1, height_segments=1, direction='+z', vertex_colors=None, face_colors=None, color=(0.5, 0.5, 1, 1), edge_color=None):
        vertices, filled_indices, outline_indices = create_plane(width, height, width_segments, height_segments, direction)
        self._mesh = MeshVisual(vertices['position'], filled_indices, vertex_colors, face_colors, color)
        self._mesh.update_gl_state(polygon_offset=(1, 1), polygon_offset_fill=True)
        self._outline = None
        CompoundVisual.__init__(self, [self._mesh])
        if edge_color:
            self._outline = MeshVisual(vertices['position'], outline_indices, color=edge_color, mode='lines')
            self.add_subvisual(self._outline)