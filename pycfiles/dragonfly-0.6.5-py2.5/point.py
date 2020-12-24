# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\point.py
# Compiled at: 2008-12-01 01:43:53
"""
    This file implements a Point class for geometry operations.
"""

class Point(object):

    def __init__(self, x=None, y=None):
        self._x = 0.0
        self._y = 0.0
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        return

    def copy(self):
        return Point(x=self._x, y=self._y)

    def __copy__(self):
        return self.copy()

    def __str__(self):
        return '%s(%.2f,%.2f)' % (self.__class__.__name__, self._x, self._y)

    def _set_x(self, x):
        if isinstance(x, float):
            self._x = x
        elif isinstance(x, int):
            self._x = float(x)
        else:
            raise TypeError('Point coordinate must be an int or float; received %r.' % x)

    x = property(fget=lambda self: self._x, fset=_set_x, doc='Protected access to x attribute.')

    def _set_y(self, y):
        if isinstance(y, float):
            self._y = y
        elif isinstance(y, int):
            self._y = float(y)
        else:
            raise TypeError('Point coordinate must be an int or float; received %r.' % y)

    y = property(fget=lambda self: self._y, fset=_set_y, doc='Protected access to y attribute.')

    def __iadd__(self, other):
        """Translate point by adding another point's coordinates."""
        if not isinstance(other, Point):
            return NotImplemented
        self._x += other._x
        self._y += other._y
        return self

    def __add__(self, other):
        """Create a new point with coordinates of this point and other
            added up."""
        if not isinstance(other, Point):
            return NotImplemented
        clone = self.copy()
        clone += other
        return clone

    def translate(self, dx, dy):
        """camp point."""
        other = Point(dx, dy)
        self += other

    def interpolate(self, other, fraction):
        """Create a new point with coordinates interpolated between
            this point and another."""
        if not isinstance(other, Point):
            raise TypeError('Can only interpolate between points; received %r' % other)
        x1 = self._x
        y1 = self._y
        x2 = other._x
        y2 = other._y
        x3 = x1 + (x2 - x1) * fraction
        y3 = y1 + (y2 - y1) * fraction
        return Point(x3, y3)

    def average(self, other):
        """Translate point."""
        return self.interpolate(other, 0.5)

    def renormalize(self, src, dst):
        nx = (self._x - src.x1) / src.dx
        self._x = dst.x1 + nx * dst.dx
        ny = (self._y - src.y1) / src.dy
        self._y = dst.y1 + ny * dst.dy
        return self