# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/scene/cameras/arcball.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 3366 bytes
from __future__ import division
import numpy as np
from util.quaternion import Quaternion
from visuals.transforms import MatrixTransform
from .perspective import Base3DRotationCamera

class ArcballCamera(Base3DRotationCamera):
    __doc__ = ' 3D camera class that orbits around a center point while\n    maintaining a view on a center point.\n\n    For this camera, the ``scale_factor`` indicates the zoom level, and\n    the ``center`` indicates the position to put at the center of the\n    view.\n\n    Parameters\n    ----------\n    fov : float\n        Field of view. Zero (default) means orthographic projection.\n    distance : float | None\n        The distance of the camera from the rotation point (only makes sense\n        if fov > 0). If None (default) the distance is determined from the\n        scale_factor and fov.\n    **kwargs : dict\n        Keyword arguments to pass to `BaseCamera`.\n\n    Notes\n    -----\n    Interaction:\n\n        * LMB: orbits the view around its center point.\n        * RMB or scroll: change scale_factor (i.e. zoom level)\n        * SHIFT + LMB: translate the center point\n        * SHIFT + RMB: change FOV\n\n    '
    _state_props = Base3DRotationCamera._state_props

    def __init__(self, fov=0.0, distance=None, **kwargs):
        (super(ArcballCamera, self).__init__)(fov=fov, **kwargs)
        self._quaternion = Quaternion()
        self.distance = distance

    def _update_rotation(self, event):
        """Update rotation parmeters based on mouse movement"""
        p2 = event.mouse_event.pos
        if self._event_value is None:
            self._event_value = p2
        wh = self._viewbox.size
        self._quaternion = Quaternion(*_arcball(p2, wh)) * Quaternion(*_arcball(self._event_value, wh)) * self._quaternion
        self._event_value = p2
        self.view_changed()

    def _rotate_tr(self):
        """Rotate the transformation matrix based on camera parameters"""
        rot, x, y, z = self._quaternion.get_axis_angle()
        up, forward, right = self._get_dim_vectors()
        self.transform.rotate(180 * rot / np.pi, (x, z, y))

    def _dist_to_trans(self, dist):
        """Convert mouse x, y movement into x, y, z translations"""
        rot, x, y, z = self._quaternion.get_axis_angle()
        tr = MatrixTransform()
        tr.rotate(180 * rot / np.pi, (x, y, z))
        dx, dz, dy = np.dot(tr.matrix[:3, :3], (dist[0], dist[1], 0.0))
        return (dx, dy, dz)

    def _get_dim_vectors(self):
        return np.eye(3)[::-1]


def _arcball(xy, wh):
    """Convert x,y coordinates to w,x,y,z Quaternion parameters

    Adapted from:

    linalg library

    Copyright (c) 2010-2015, Renaud Blanch <rndblnch at gmail dot com>
    Licence at your convenience:
    GPLv3 or higher <http://www.gnu.org/licenses/gpl.html>
    BSD new <http://opensource.org/licenses/BSD-3-Clause>
    """
    x, y = xy
    w, h = wh
    r = (w + h) / 2.0
    x, y = -(2.0 * x - w) / r, (2.0 * y - h) / r
    h = np.sqrt(x * x + y * y)
    if h > 1.0:
        return (0.0, x / h, y / h, 0.0)
    return (0.0, x, y, np.sqrt(1.0 - h * h))