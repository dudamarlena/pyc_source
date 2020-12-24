# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/ellipse.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 5533 bytes
"""
Simple ellipse visual based on PolygonVisual
"""
from __future__ import division
import numpy as np
from .polygon import PolygonVisual

class EllipseVisual(PolygonVisual):
    __doc__ = '\n    Displays a 2D ellipse\n\n    Parameters\n    ----------\n    center : array\n        Center of the ellipse\n    color : instance of Color\n        The face color to use.\n    border_color : instance of Color\n        The border color to use.\n    border_width: float\n        The width of the border in pixels\n    radius : float | tuple\n        Radius or radii of the ellipse\n        Defaults to  (0.1, 0.1)\n    start_angle : float\n        Start angle of the ellipse in degrees\n        Defaults to 0.\n    span_angle : float\n        Span angle of the ellipse in degrees\n        Defaults to 0.\n    num_segments : int\n        Number of segments to be used to draw the ellipse\n        Defaults to 100\n    '

    def __init__(self, center=None, color='black', border_color=None, border_width=1, radius=(0.1, 0.1), start_angle=0.0, span_angle=360.0, num_segments=100, **kwargs):
        self._center = center
        self._radius = radius
        self._start_angle = start_angle
        self._span_angle = span_angle
        self._num_segments = num_segments
        (PolygonVisual.__init__)(self, pos=None, color=color, border_color=border_color, 
         border_width=border_width, **kwargs)
        self._mesh.mode = 'triangle_fan'
        self._update()

    @staticmethod
    def _generate_vertices(center, radius, start_angle, span_angle, num_segments):
        if isinstance(radius, (list, tuple)):
            if len(radius) == 2:
                xr, yr = radius
            else:
                raise ValueError('radius must be float or 2 value tuple/list (got %s of length %d)' % (
                 type(radius),
                 len(radius)))
        else:
            xr = yr = radius
        start_angle = np.deg2rad(start_angle)
        vertices = np.empty([num_segments + 2, 2], dtype=(np.float32))
        theta = np.linspace(start_angle, start_angle + np.deg2rad(span_angle), num_segments + 1)
        vertices[:-1, 0] = center[0] + xr * np.cos(theta)
        vertices[:-1, 1] = center[1] + yr * np.sin(theta)
        vertices[num_segments + 1] = np.float32([center[0], center[1]])
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
    def radius(self):
        """ The start radii of the ellipse.
        """
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        self._update()

    @property
    def start_angle(self):
        """ The start start_angle of the ellipse.
        """
        return self._start_angle

    @start_angle.setter
    def start_angle(self, start_angle):
        self._start_angle = start_angle
        self._update()

    @property
    def span_angle(self):
        """ The angular span of the ellipse.
        """
        return self._span_angle

    @span_angle.setter
    def span_angle(self, span_angle):
        self._span_angle = span_angle
        self._update()

    @property
    def num_segments(self):
        """ The number of segments in the ellipse.
        """
        return self._num_segments

    @num_segments.setter
    def num_segments(self, num_segments):
        num_segments = int(num_segments)
        if num_segments < 1:
            raise ValueError('EllipseVisual must consist of more than 1 segment')
        self._num_segments = num_segments
        self._update()

    def _update(self):
        if self._center is None:
            return
        else:
            vertices = self._generate_vertices(center=(self._center), radius=(self._radius),
              start_angle=(self._start_angle),
              span_angle=(self._span_angle),
              num_segments=(self._num_segments))
            if not self._color.is_blank:
                self._mesh.set_data(vertices=vertices, color=(self._color.rgba))
            border_pos = self._border_color.is_blank or vertices[:-1]
            self._border.set_data(pos=border_pos, color=(self._border_color.rgba),
              width=(self._border_width),
              connect='strip')