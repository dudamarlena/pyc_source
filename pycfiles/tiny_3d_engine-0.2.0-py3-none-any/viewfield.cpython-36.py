# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/viewfield.py
# Compiled at: 2020-04-23 14:49:36
# Size of source mod 2**32: 3437 bytes
"""
Field of Vision
---------------

Here are the rotation and projection for a point.

In this world, points are in a non-dimensional space,
relative to the point of view.
Coordinates changes, and can switch, upon the dialog with the user.

"""
import numpy as np
from tiny_3d_engine.scene3d import comp_min_max
__all__ = [
 'ViewField']
FLOAT = np.float32

class ViewField:

    def __init__(self, width, height):
        """Initiate the view field

        :param width: x_size of canvas
        :param height: y_size of canvas
                """
        self.zeros = (
         0.5 * width, 0.5 * height)
        self.init_scale = 0.2 * (width + height)
        self.center = None
        self.size = None
        self.pts = None
        self.min = None
        self.max = None

    def update(self, points):
        """Update the points inside the viewfield

        :param points: numpy array of size (n,3)
        """
        self.min, self.max = comp_min_max(points)
        self.center = 0.5 * (self.min + self.max)
        self.size = 0.5 * np.amax((self.max - self.min), axis=0)
        self.center = 0.5 * (self.min + self.max).astype(FLOAT)
        self.pts = (points - self.center[np.newaxis, :]).astype(FLOAT) / self.size

    def flatten(self, distance, scale):
        """calculate 2D coordinates from 3D point"""
        proj = np.zeros((self.pts.shape[0], 2), dtype=FLOAT)
        proj[:, 0] = self.zeros[0] - scale * (self.pts[:, 0] * distance / (self.pts[:, 2] + distance))
        proj[:, 1] = self.zeros[1] - scale * (self.pts[:, 1] * distance / (self.pts[:, 2] + distance))
        return proj.astype(int)

    def rotate(self, axis, angle):
        """rotate point around axis"""
        angle = angle / 180 * np.pi
        new_pts = np.zeros_like((self.pts), dtype=FLOAT)
        if axis == 'z':
            new_pts[:, 0] = self.pts[:, 0] * np.cos(angle) - self.pts[:, 1] * np.sin(angle)
            new_pts[:, 1] = self.pts[:, 1] * np.cos(angle) + self.pts[:, 0] * np.sin(angle)
            new_pts[:, 2] = self.pts[:, 2]
        else:
            if axis == 'x':
                new_pts[:, 0] = self.pts[:, 0]
                new_pts[:, 1] = self.pts[:, 1] * np.cos(angle) - self.pts[:, 2] * np.sin(angle)
                new_pts[:, 2] = self.pts[:, 2] * np.cos(angle) + self.pts[:, 1] * np.sin(angle)
            else:
                if axis == 'y':
                    new_pts[:, 0] = self.pts[:, 0] * np.cos(angle) - self.pts[:, 2] * np.sin(angle)
                    new_pts[:, 1] = self.pts[:, 1]
                    new_pts[:, 2] = self.pts[:, 2] * np.cos(angle) + self.pts[:, 0] * np.sin(angle)
                else:
                    raise ValueError('not a valid axis')
        self.pts = new_pts

    def translate(self, axis, amount):
        """tranlate point by distance"""
        new_pts = np.array((self.pts), dtype=FLOAT)
        if axis == 'z':
            new_pts[:, 2] += amount
        else:
            if axis == 'x':
                new_pts[:, 0] += amount
            else:
                if axis == 'y':
                    new_pts[:, 1] += amount
                else:
                    raise ValueError('not a valid axis')
        self.pts = new_pts