# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/scene/cameras/turntable.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 5029 bytes
from __future__ import division
import numpy as np
from .perspective import Base3DRotationCamera

class TurntableCamera(Base3DRotationCamera):
    __doc__ = ' 3D camera class that orbits around a center point while\n    maintaining a view on a center point.\n\n    For this camera, the ``scale_factor`` indicates the zoom level, and\n    the ``center`` indicates the position to put at the center of the\n    view.\n\n    Parameters\n    ----------\n    fov : float\n        Field of view. Zero (default) means orthographic projection.\n    elevation : float\n        Elevation angle in degrees. Positive angles place the camera\n        above the cente point, negative angles place the camera below\n        the center point.\n    azimuth : float\n        Azimuth angle in degrees. Zero degrees places the camera on the\n        positive x-axis, pointing in the negative x direction.\n    roll : float\n        Roll angle in degrees\n    distance : float | None\n        The distance of the camera from the rotation point (only makes sense\n        if fov > 0). If None (default) the distance is determined from the\n        scale_factor and fov.\n    **kwargs : dict\n        Keyword arguments to pass to `BaseCamera`.\n\n    Notes\n    -----\n    Interaction:\n\n        * LMB: orbits the view around its center point.\n        * RMB or scroll: change scale_factor (i.e. zoom level)\n        * SHIFT + LMB: translate the center point\n        * SHIFT + RMB: change FOV\n\n    '
    _state_props = Base3DRotationCamera._state_props + ('elevation', 'azimuth', 'roll')

    def __init__(self, fov=0.0, elevation=30.0, azimuth=30.0, roll=0.0, distance=None, **kwargs):
        super(TurntableCamera, self).__init__(fov=fov, **kwargs)
        self.azimuth = azimuth
        self.elevation = elevation
        self.roll = roll
        self.distance = distance

    @property
    def elevation(self):
        """ The angle of the camera in degrees above the horizontal (x, z)
        plane.
        """
        return self._elevation

    @elevation.setter
    def elevation(self, elev):
        elev = float(elev)
        self._elevation = min(90, max(-90, elev))
        self.view_changed()

    @property
    def azimuth(self):
        """ The angle of the camera in degrees around the y axis. An angle of
        0 places the camera within the (y, z) plane.
        """
        return self._azimuth

    @azimuth.setter
    def azimuth(self, azim):
        azim = float(azim)
        while azim < -180:
            azim += 360

        while azim > 180:
            azim -= 360

        self._azimuth = azim
        self.view_changed()

    @property
    def roll(self):
        """ The angle of the camera in degrees around the z axis. An angle of
        0 places puts the camera upright.
        """
        return self._roll

    @roll.setter
    def roll(self, roll):
        roll = float(roll)
        while roll < -180:
            roll += 360

        while roll > 180:
            roll -= 360

        self._roll = roll
        self.view_changed()

    def orbit(self, azim, elev):
        """ Orbits the camera around the center position.

        Parameters
        ----------
        azim : float
            Angle in degrees to rotate horizontally around the center point.
        elev : float
            Angle in degrees to rotate vertically around the center point.
        """
        self.azimuth += azim
        self.elevation = np.clip(self.elevation + elev, -90, 90)
        self.view_changed()

    def _update_rotation(self, event):
        """Update rotation parmeters based on mouse movement"""
        p1 = event.mouse_event.press_event.pos
        p2 = event.mouse_event.pos
        if self._event_value is None:
            self._event_value = (
             self.azimuth, self.elevation)
        self.azimuth = self._event_value[0] - (p2 - p1)[0] * 0.5
        self.elevation = self._event_value[1] + (p2 - p1)[1] * 0.5

    def _rotate_tr(self):
        """Rotate the transformation matrix based on camera parameters"""
        up, forward, right = self._get_dim_vectors()
        self.transform.rotate(self.elevation, -right)
        self.transform.rotate(self.azimuth, up)

    def _dist_to_trans(self, dist):
        """Convert mouse x, y movement into x, y, z translations"""
        rae = np.array([self.roll, self.azimuth, self.elevation]) * np.pi / 180
        sro, saz, sel = np.sin(rae)
        cro, caz, cel = np.cos(rae)
        dx = +dist[0] * (cro * caz + sro * sel * saz) + dist[1] * (sro * caz - cro * sel * saz)
        dy = +dist[0] * (cro * saz - sro * sel * caz) + dist[1] * (sro * saz + cro * sel * caz)
        dz = -dist[0] * sro * cel + dist[1] * cro * cel
        return (dx, dy, dz)