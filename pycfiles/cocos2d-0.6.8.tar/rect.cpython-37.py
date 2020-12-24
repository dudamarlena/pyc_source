# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\rect.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 11711 bytes
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'

class Rect(object):
    __doc__ = 'Define a rectangular area.\n\n    Many convenience handles and other properties are also defined - all of\n    which may be assigned to which will result in altering the position\n    and sometimes dimensions of the Rect:\n\n        - top         -- y pixel extent\n        - bottom      -- y pixel extent\n        - left        -- x pixel extent\n        - right       -- x pixel extent\n        - position    -- (x, y) of bottom-left corner pixel\n        - origin      -- (x, y) of bottom-left corner pixel\n        - center      -- (x, y) of center pixel\n        - topleft     -- (x, y) of top-left corner pixel\n        - topright    -- (x, y) of top-right corner pixel\n        - bottomleft  -- (x, y) of bottom-left corner pixel\n        - bottomright -- (x, y) of bottom-right corner pixel\n        - midtop      -- (x, y) of middle of top side pixel\n        - midbottom   -- (x, y) of middle of bottom side pixel\n        - midleft     -- (x, y) of middle of left side pixel\n        - midright    -- (x, y) of middle of right side pixel\n        - size        -- (width, height) of rect\n\n    The Rect area includes the bottom and left borders but not the top and\n    right borders.\n    '

    def __init__(self, x, y, width, height):
        """Create a Rect with the bottom-left corner at (x, y) and
        dimensions (width, height).
        """
        self._x, self._y = x, y
        self._width, self._height = width, height

    def __nonzero__(self):
        return bool(self.width and self.height)

    def __repr__(self):
        return 'Rect(xy=%.4g,%.4g; wh=%.4g,%.4g)' % (self.x, self.y,
         self.width, self.height)

    def __eq__(self, other):
        """Compare the two rects.

        >>> r1 = Rect(0, 0, 10, 10)
        >>> r1 == Rect(0, 0, 10, 10)
        True
        >>> r1 == Rect(1, 0, 10, 10)
        False
        >>> r1 == Rect(0, 1, 10, 10)
        False
        >>> r1 == Rect(0, 0, 11, 10)
        False
        >>> r1 == Rect(0, 0, 10, 11)
        False
        """
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    __hash__ = object.__hash__

    def __ne__(self, other):
        """Compare the two rects.

        >>> r1 = Rect(0, 0, 10, 10)
        >>> r1 != Rect(0, 0, 10, 10)
        False
        >>> r1 != Rect(1, 0, 10, 10)
        True
        >>> r1 != Rect(0, 1, 10, 10)
        True
        >>> r1 != Rect(0, 0, 11, 10)
        True
        >>> r1 != Rect(0, 0, 10, 11)
        True
        """
        return not self == other

    def copy(self):
        return self.__class__(self.x, self.y, self.width, self.height)

    def set_x(self, value):
        self._x = value

    x = property(lambda self: self._x, set_x)

    def set_y(self, value):
        self._y = value

    y = property(lambda self: self._y, set_y)

    def set_width(self, value):
        self._width = value

    width = property(lambda self: self._width, set_width)

    def set_height(self, value):
        self._height = value

    height = property(lambda self: self._height, set_height)

    def contains(self, x, y):
        """Return boolean whether the point defined by x, y is inside the
        rect area.
        """
        if x < self.x or x > self.x + self.width:
            return False
        if y < self.y or y > self.y + self.height:
            return False
        return True

    def intersects(self, other):
        """Return boolean whether the interior of "other" rect (an object 
        with .x, .y, .width and .height attributes) overlaps the interior
        of this Rect in any way.
        """
        if self.x + self.width <= other.x:
            return False
        if other.x + other.width <= self.x:
            return False
        if self.y + self.height <= other.y:
            return False
        if other.y + other.height <= self.y:
            return False
        return True

    def clippedBy(self, other):
        """bool. True iif intersection with other is smaller than self.

        Equivalent: True if self doesn't fit entirely into other

        >>> r1 = Rect(0, 0, 10, 10)
        >>> r2 = Rect(1, 1, 9, 9)
        >>> r2.clippedBy(r1)    # r2 fits inside r1
        False
        >>> r1.clippedBy(r2)    # r1 is clipped by r2
        True
        >>> r2 = Rect(1, 1, 11, 11)
        >>> r1.intersect(r2)
        Rect(xy=1,1; wh=9,9)
        >>> r1.clippedBy(r2)
        True
        >>> r2.intersect(r1)
        Rect(xy=1,1; wh=9,9)
        >>> r2.clippedBy(r1)
        True
        >>> r2 = Rect(11, 11, 1, 1)
        >>> r1.clippedBy(r2)
        True
        """
        intersection = self.intersect(other)
        if intersection is None:
            return True
        return intersection != self

    def intersect(self, other):
        """Find the intersection of two Rect s.

        >>> r1 = Rect(0, 51, 200, 17)
        >>> r2 = Rect(0, 64, 200, 55)
        >>> r1.intersect(r2)
        Rect(xy=0,64; wh=200,4)

        >>> r1 = Rect(0, 64, 200, 55)
        >>> r2 = Rect(0, 0, 200, 17)
        >>> print r1.intersect(r2)
        None

        >>> r1 = Rect(10, 10, 10, 10)
        >>> r2 = Rect(20, 20, 10, 10)
        >>> print r1.intersect(r2)
        None

        >>> bool(Rect(0, 0, 1, 1))
        True
        >>> bool(Rect(0, 0, 1, 0))
        False
        >>> bool(Rect(0, 0, 0, 1))
        False
        >>> bool(Rect(0, 0, 0, 0))
        False
        """
        s_tr_x, s_tr_y = self.topright
        o_tr_x, o_tr_y = other.topright
        bl_x = max(self.x, other.x)
        bl_y = max(self.y, other.y)
        tr_x = min(s_tr_x, o_tr_x)
        tr_y = min(s_tr_y, o_tr_y)
        w, h = max(0, tr_x - bl_x), max(0, tr_y - bl_y)
        return w and h or None
        return self.__class__(bl_x, bl_y, w, h)

    def set_position(self, value):
        self._x, self._y = value

    position = property(lambda self: (self._x, self._y), set_position)

    def set_size(self, value):
        self._width, self._height = value

    size = property(lambda self: (self._width, self._height), set_size)

    def get_origin(self):
        return (
         self.x, self.y)

    def set_origin(self, origin):
        self.x, self.y = origin

    origin = property(get_origin, set_origin)

    def get_top(self):
        return self.y + self.height

    def set_top(self, y):
        self.y = y - self.height

    top = property(get_top, set_top)

    def get_bottom(self):
        return self.y

    def set_bottom(self, y):
        self.y = y

    bottom = property(get_bottom, set_bottom)

    def get_left(self):
        return self.x

    def set_left(self, x):
        self.x = x

    left = property(get_left, set_left)

    def get_right(self):
        return self.x + self.width

    def set_right(self, x):
        self.x = x - self.width

    right = property(get_right, set_right)

    def get_center(self):
        return (
         self.x + self.width // 2, self.y + self.height // 2)

    def set_center(self, center):
        x, y = center
        self.position = (x - self.width // 2, y - self.height // 2.0)

    center = property(get_center, set_center)

    def get_midtop(self):
        return (
         self.x + self.width // 2, self.y + self.height)

    def set_midtop(self, midtop):
        x, y = midtop
        self.position = (x - self.width // 2, y - self.height)

    midtop = property(get_midtop, set_midtop)

    def get_midbottom(self):
        return (
         self.x + self.width // 2, self.y)

    def set_midbottom(self, midbottom):
        x, y = midbottom
        self.position = (x - self.width // 2, y)

    midbottom = property(get_midbottom, set_midbottom)

    def get_midleft(self):
        return (
         self.x, self.y + self.height // 2)

    def set_midleft(self, midleft):
        x, y = midleft
        self.position = (x, y - self.height // 2)

    midleft = property(get_midleft, set_midleft)

    def get_midright(self):
        return (
         self.x + self.width, self.y + self.height // 2)

    def set_midright(self, midright):
        x, y = midright
        self.position = (x - self.width, y - self.height // 2)

    midright = property(get_midright, set_midright)

    def get_topleft(self):
        return (
         self.x, self.y + self.height)

    def set_topleft(self, position):
        x, y = position
        self.position = (x, y - self.height)

    topleft = property(get_topleft, set_topleft)

    def get_topright(self):
        return (
         self.x + self.width, self.y + self.height)

    def set_topright(self, position):
        x, y = position
        self.position = (x - self.width, y - self.height)

    topright = property(get_topright, set_topright)

    def get_bottomright(self):
        return (
         self.x + self.width, self.y)

    def set_bottomright(self, position):
        x, y = position
        self.position = (x - self.width, y)

    bottomright = property(get_bottomright, set_bottomright)

    def get_bottomleft(self):
        return (
         self.x, self.y)

    def set_bottomleft(self, position):
        self.x, self.y = position

    bottomleft = property(get_bottomleft, set_bottomleft)