# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\camera.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 5425 bytes
__doc__ = 'Camera object'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from pyglet import gl
import cocos.director as director
from cocos.euclid import Point3
__all__ = [
 'Camera']

class Camera(object):
    """Camera"""

    def __init__(self):
        self.restore()

    @classmethod
    def get_z_eye(cls):
        """Returns the best distance for the camera for the current window size

        cocos2d uses a Filed Of View (fov) of 60
        """
        width, height = director.get_window_size()
        eye_z = height / 1.1566
        return eye_z

    def restore(self):
        """Restore the camera to the initial position
        and sets it's ``dirty`` attribute in False and ``once`` in true.

        If you use the camera, for a while and you want to stop using it
        call this method.
        """
        width, height = director.get_window_size()
        self._eye = Point3(width / 2.0, height / 2.0, self.get_z_eye())
        self._center = Point3(width / 2.0, height / 2.0, 0.0)
        self._up_vector = Point3(0.0, 1.0, 0.0)
        self.dirty = False
        self.once = False

    def locate(self, force=False):
        """Sets the camera using gluLookAt using its eye, center and up_vector

        :Parameters:
            `force` : bool
                whether or not the camera will be located even if it is not dirty
        """
        if force or self.dirty or self.once:
            gl.glLoadIdentity()
            gl.gluLookAt(self._eye.x, self._eye.y, self._eye.z, self._center.x, self._center.y, self._center.z, self._up_vector.x, self._up_vector.y, self._up_vector.z)
            self.once = False

    def _get_eye(self):
        return self._eye

    def _set_eye(self, eye):
        self._eye = eye
        self.dirty = True

    eye = property(_get_eye, _set_eye, doc='Eye of the camera in x,y,z coordinates\n\n    :type: float,float,float\n    ')

    def _get_center(self):
        return self._center

    def _set_center(self, center):
        self._center = center
        self.dirty = True

    center = property(_get_center, _set_center, doc='Center of the camera in x,y,z coordinates\n\n    :type: float,float,float\n    ')

    def _get_up_vector(self):
        return self._up_vector

    def _set_up_vector(self, up_vector):
        self._up_vector = up_vector
        self.dirty = True

    up_vector = property(_get_up_vector, _set_up_vector, doc='Up vector of the camera in x,y,z coordinates\n\n    :type: float,float,float\n    ')