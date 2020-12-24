# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/rectangle.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 7493 bytes
"""
Simple ellipse visual based on PolygonVisual
"""
from __future__ import division
import numpy as np
from ..color import Color
from .polygon import PolygonVisual

class RectangleVisual(PolygonVisual):
    __doc__ = '\n    Displays a 2D rectangle with optional rounded corners\n\n    Parameters\n    ----------\n    center :  array\n        Center of the rectangle\n    color : instance of Color\n        The fill color to use.\n    border_color : instance of Color\n        The border color to use.\n    border_width : int\n        Border width in pixels.\n    height : float\n        Length of the rectangle along y-axis\n        Defaults to 1.0\n    width : float\n        Length of the rectangle along x-axis\n        Defaults to 1.0\n    radius : float | array\n        Radii of curvatures of corners in clockwise order from top-left\n        Defaults to 0.\n    '

    def __init__(self, center=None, color='black', border_color=None, border_width=1, height=1.0, width=1.0, radius=[
 0.0, 0.0, 0.0, 0.0], **kwargs):
        self._height = height
        self._width = width
        self._color = Color(color)
        self._border_color = Color(border_color)
        self._border_width = border_width
        self._radius = None
        self.center = None
        PolygonVisual.__init__(self, pos=None, color=color, border_color=border_color, border_width=border_width, **kwargs)
        self.radius = radius
        self.center = center
        self._mesh.mode = 'triangle_fan'
        self._update()

    def _generate_vertices(self, center, radius, height, width):
        half_height = self._height / 2.0
        half_width = self._width / 2.0
        hw = min(half_height, half_width)
        num_segments = (radius / hw * 500.0).astype(int)
        bias1 = np.ones(4) * half_width - radius
        bias2 = np.ones(4) * half_height - radius
        corner1 = np.empty([num_segments[0] + 1, 3], dtype=np.float32)
        corner2 = np.empty([num_segments[1] + 1, 3], dtype=np.float32)
        corner3 = np.empty([num_segments[2] + 1, 3], dtype=np.float32)
        corner4 = np.empty([num_segments[3] + 1, 3], dtype=np.float32)
        start_angle = 0.0
        end_angle = np.pi / 2.0
        theta = np.linspace(end_angle, start_angle, num_segments[0] + 1)
        corner1[:, 0] = center[0] - bias1[0] - radius[0] * np.sin(theta)
        corner1[:, 1] = center[1] - bias2[0] - radius[0] * np.cos(theta)
        corner1[:, 2] = 0
        theta = np.linspace(start_angle, end_angle, num_segments[1] + 1)
        corner2[:, 0] = center[0] + bias1[1] + radius[1] * np.sin(theta)
        corner2[:, 1] = center[1] - bias2[1] - radius[1] * np.cos(theta)
        corner2[:, 2] = 0
        theta = np.linspace(end_angle, start_angle, num_segments[2] + 1)
        corner3[:, 0] = center[0] + bias1[2] + radius[2] * np.sin(theta)
        corner3[:, 1] = center[1] + bias2[2] + radius[2] * np.cos(theta)
        corner3[:, 2] = 0
        theta = np.linspace(start_angle, end_angle, num_segments[3] + 1)
        corner4[:, 0] = center[0] - bias1[3] - radius[3] * np.sin(theta)
        corner4[:, 1] = center[1] + bias2[3] + radius[3] * np.cos(theta)
        corner4[:, 2] = 0
        output = np.concatenate(([[center[0], center[1], 0.0]],
         [
          [
           center[0] - half_width, center[1], 0.0]],
         corner1,
         [
          [
           center[0], center[1] - half_height, 0.0]],
         corner2,
         [
          [
           center[0] + half_width, center[1], 0.0]],
         corner3,
         [
          [
           center[0], center[1] + half_height, 0.0]],
         corner4,
         [
          [
           center[0] - half_width, center[1], 0.0]]))
        vertices = np.array(output, dtype=np.float32)
        return vertices

    @property
    def center(self):
        """ The center of the ellipse
        """
        return self._center

    @center.setter
    def center(self, center):
        """ The center of the ellipse
        """
        self._center = center
        self._update()

    @property
    def height(self):
        """ The height of the rectangle.
        """
        return self._height

    @height.setter
    def height(self, height):
        if height <= 0.0:
            raise ValueError('Height must be positive')
        self._height = height
        self._update()

    @property
    def width(self):
        """ The width of the rectangle.
        """
        return self._width

    @width.setter
    def width(self, width):
        if width <= 0.0:
            raise ValueError('Width must be positive')
        self._width = width
        self._update()

    @property
    def radius(self):
        """ The radius of curvature of rounded corners.
        """
        return self._radius

    @radius.setter
    def radius(self, radius):
        half_height = self._height / 2.0
        half_width = self._width / 2.0
        hw = min(half_height, half_width)
        if isinstance(radius, (list, tuple)):
            if len(radius) != 4:
                raise ValueError('radius must be float or 4 value tuple/list (got %s of length %d)' % (
                 type(radius),
                 len(radius)))
            if (radius > np.ones(4) * hw).all():
                raise ValueError('Radius of curvature cannot be greater than                                  half of min(width, height)')
            radius = np.array(radius, dtype=np.float32)
        else:
            if radius > hw:
                raise ValueError('Radius of curvature cannot be greater than                                  half of min(width, height)')
            radius = np.ones(4) * radius
        self._radius = radius
        self._update()

    def _update(self):
        if not self._center:
            return
        if self._radius is None:
            return
        vertices = self._generate_vertices(center=self._center, radius=self._radius, height=self._height, width=self._width)
        self._pos = vertices
        if not self._color.is_blank:
            self.mesh.set_data(vertices=vertices, color=self._color.rgba)
        if not self._border_color.is_blank:
            self.border.set_data(pos=vertices[1:, ..., :2], color=self._border_color.rgba)