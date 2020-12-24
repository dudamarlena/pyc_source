# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\graphic_lib\Font\Glyph.py
# Compiled at: 2020-03-15 07:19:57
# Size of source mod 2**32: 324 bytes


class Glyph:

    def __init__(self, glyph):
        self.glyph_ = glyph
        self.width_ = max((len(line) for line in glyph))
        self.height_ = len(glyph)

    def width(self):
        return self.width_

    def height(self):
        return self.height_

    def glyph(self):
        return self.glyph_