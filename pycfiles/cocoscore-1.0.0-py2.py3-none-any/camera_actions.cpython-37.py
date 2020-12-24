# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\actions\camera_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 6490 bytes
__doc__ = 'Camera Actions\n\nActions that moves the OpenGL camera.\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import cocos.director as director
from cocos.euclid import *
from .base_actions import *
import math
__all__ = [
 'CameraException',
 'Camera3DAction',
 'OrbitCamera']

class CameraException(Exception):
    pass


class Camera3DAction(IntervalAction):

    def init(self, duration=2):
        """Initialize the Camera Action

        :Parameters:
            `duration` : int
                Number of seconds that the action will last
        """
        self.duration = duration

    def start(self):
        super(Camera3DAction, self).start()
        self.camera_eye_orig = self.target.camera.eye
        self.camera_center_orig = self.target.camera.center
        self.camera_up_orig = self.target.camera.up_vector

    def __reversed__(self):
        return _ReverseTime(self)


class OrbitCamera(Camera3DAction):
    """OrbitCamera"""

    def init(self, radius=None, delta_radius=0, angle_z=None, delta_z=0, angle_x=None, delta_x=0, *args, **kw):
        """Initialize the camera with spherical coordinates

        :Parameters:
            `radius` : float
                Radius of the orbit. Default: current radius
            `delta_radius` : float
                Delta movement of the radius. Default: 0
            `angle_z` : float
                The zenith angle of the spherical coordinate in degrees. Default: current
            `delta_z` : float
                Relative movement of the zenith angle. Default: 0
            `angle_x` : float
                The azimuth angle of the spherical coordinate in degrees. Default: 0
            `delta_x` : float
                Relative movement of the azimuth angle. Default: 0

        For more information regarding spherical coordinates, read this:
            http://en.wikipedia.org/wiki/Spherical_coordinates

        """
        (super(OrbitCamera, self).init)(*args, **kw)
        width, height = director.get_window_size()
        self.radius = radius
        self.delta_radius = delta_radius
        self.angle_x = angle_x
        self.rad_delta_x = math.radians(delta_x)
        self.angle_z = angle_z
        self.rad_delta_z = math.radians(delta_z)

    def start(self):
        super(OrbitCamera, self).start()
        radius, zenith, azimuth = self.get_spherical_coords()
        if self.radius is None:
            self.radius = radius
        if self.angle_z is None:
            self.angle_z = math.degrees(zenith)
        if self.angle_x is None:
            self.angle_x = math.degrees(azimuth)
        self.rad_x = math.radians(self.angle_x)
        self.rad_z = math.radians(self.angle_z)

    def get_spherical_coords(self):
        """returns the spherical coordinates from a cartesian coordinates

        using this formula:

            - http://www.math.montana.edu/frankw/ccp/multiworld/multipleIVP/spherical/body.htm#converting

        :rtype: (radius, zenith, azimuth)
        """
        eye = self.target.camera.eye - self.target.camera.center
        radius = math.sqrt(pow(eye.x, 2) + pow(eye.y, 2) + pow(eye.z, 2))
        s = math.sqrt(pow(eye.x, 2) + pow(eye.y, 2))
        if s == 0:
            s = 1e-09
        else:
            r = radius
            if r == 0:
                r = 1e-09
            angle_z = math.acos(eye.z / r)
            if eye.x < 0:
                angle_x = math.pi - math.asin(eye.y / s)
            else:
                angle_x = math.asin(eye.y / s)
        radius = radius / self.target.camera.get_z_eye()
        return (
         radius, angle_z, angle_x)

    def update(self, t):
        r = (self.radius + self.delta_radius * t) * self.target.camera.get_z_eye()
        z_angle = self.rad_z + self.rad_delta_z * t
        x_angle = self.rad_x + self.rad_delta_x * t
        p = Point3(math.sin(z_angle) * math.cos(x_angle), math.sin(z_angle) * math.sin(x_angle), math.cos(z_angle))
        p = p * r
        d = p + self.camera_center_orig
        self.target.camera.eye = d