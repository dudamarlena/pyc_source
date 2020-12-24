# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vis2048\vec2.py
# Compiled at: 2018-10-28 10:35:01
# Size of source mod 2**32: 521 bytes


class Vec2:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)