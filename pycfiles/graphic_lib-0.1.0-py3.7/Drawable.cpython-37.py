# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\graphic_lib\detail\Drawable.py
# Compiled at: 2020-01-25 05:23:11
# Size of source mod 2**32: 1331 bytes


class Drawable:

    def __init__(self, size, default_value=0):
        self.size = size
        self.default_value = default_value
        self.height = len(size)
        self.width = max(size)
        self.framebuffer = [[default_value for _ in range(i)] for i in self.size]

    def draw(self, x_begin, y_begin, other):
        other_x_offset = 0
        self_x_offset = 0
        other_y_offset = 0
        self_y_offset = 0
        if x_begin < 0:
            other_x_offset = abs(x_begin)
        else:
            self_x_offset = abs(x_begin)
        if y_begin < 0:
            other_y_offset = abs(y_begin)
        else:
            self_y_offset = abs(y_begin)
        for y in range(len(self.size)):
            for x in range(self.size[y]):
                if y + other_y_offset < len(other.size) and y + self_y_offset < len(self.size) and x + other_x_offset < other.size[y] and x + self_x_offset < self.size[y]:
                    self.framebuffer[(y + self_y_offset)][x + self_x_offset] = other.framebuffer[(y + other_y_offset)][(x + other_x_offset)]

    def clear(self):
        for y in range(len(self.size)):
            for x in range(self.size[y]):
                self.framebuffer[y][x] = self.default_value