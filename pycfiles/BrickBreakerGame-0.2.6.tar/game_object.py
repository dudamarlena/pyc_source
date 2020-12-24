# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: BrickBreaker/Shared/game_object.py
# Compiled at: 2017-12-10 07:56:51


class GameObject:

    def __init__(self, position, size, image):
        self._position = position
        self._size = size
        self._image = image

    def set_position(self, position):
        self._position = position

    def get_position(self):
        return self._position

    def get_size(self):
        return self._size

    def get_image(self):
        return self._image

    def _intersects_x(self, other):
        other_position = other.get_position()
        other_size = other.get_size()
        if other_position[0] + other_size[0] >= self._position[0] >= other_position[0]:
            return 1
        if other_position[0] + other_size[0] >= self._position[0] + self._size[0] > other_position[0]:
            return 1
        return 0

    def _intersects_y(self, other):
        other_position = other.get_position()
        other_size = other.get_size()
        if other_position[1] + other_size[1] >= self._position[1] >= other_position[1]:
            return 1
        if other_position[1] + other_size[1] >= self._position[1] + self._size[1] > other_position[1]:
            return 1
        return 0

    def intersects(self, other):
        if self._intersects_x(other) and self._intersects_y(other):
            return 1
        return 0