# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\graphic_lib\widgets\ColorBox.py
# Compiled at: 2020-03-15 07:22:12
# Size of source mod 2**32: 446 bytes
from graphic_lib.detail import Widget

class ColorBox(Widget):

    def __init__(self, size, color):
        Widget.__init__(self, size)
        self.color = color
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def update(self):
        for y in range(len(self.size)):
            for x in range(self.size[y]):
                self.framebuffer[y][x] = self.color