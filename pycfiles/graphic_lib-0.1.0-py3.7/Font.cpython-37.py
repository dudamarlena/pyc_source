# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\graphic_lib\Font\Font.py
# Compiled at: 2020-03-15 07:19:35
# Size of source mod 2**32: 188 bytes


class MetaFont(type):

    def __getitem__(cls, symbol):
        return cls.glyphs[symbol]

    def height(cls):
        return max([glyph.height() for glyph in cls.glyphs.values()])