# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python2.7/site-packages/coloredstring/util/_protected/ColorMap.py
# Compiled at: 2016-02-29 13:04:45
from .Color import Color
__author__ = 'smt'

class ColorMap(Color):
    Black = 0
    Red = 1
    Green = 2
    Brown = 3
    Blue = 4
    Magenta = 5
    Cyan = 6
    Gray = 7
    DarkGray = 60
    LightRed = 61
    LightGreen = 62
    Yellow = 63
    LightBlue = 64
    LightMagenta = 65
    LightCyan = 66
    White = 67
    Default = 9
    _base = 0

    @classmethod
    def get_color(cls, color_code):
        if color_code == cls.Default:
            color_code = -cls._base
        return '\x1b[' + str(cls._base + color_code) + 'm'