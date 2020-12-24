# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/regular_polygon.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 1818 bytes
"""
RegularPolygonVisual visual based on EllipseVisual
"""
from __future__ import division
from .ellipse import EllipseVisual

class RegularPolygonVisual(EllipseVisual):
    __doc__ = '\n    Displays a regular polygon\n\n    Parameters\n    ----------\n\n    center : array-like (x, y)\n        Center of the regular polygon\n    color : str | tuple | list of colors\n        Fill color of the polygon\n    border_color : str | tuple | list of colors\n        Border color of the polygon\n    border_width: float\n        The width of the border in pixels\n    radius : float\n        Radius of the regular polygon\n        Defaults to  0.1\n    sides : int\n        Number of sides of the regular polygon\n    '

    def __init__(self, center=None, color='black', border_color=None, border_width=1, radius=0.1, sides=4, **kwargs):
        EllipseVisual.__init__(self, center=center, radius=radius, color=color, border_color=border_color, border_width=border_width, num_segments=sides, **kwargs)

    @property
    def sides(self):
        """ The number of sides in the regular polygon.
        """
        return self.num_segments

    @sides.setter
    def sides(self, sides):
        if sides < 3:
            raise ValueError('PolygonVisual must have at least 3 sides, not %s' % sides)
        self.num_segments = sides