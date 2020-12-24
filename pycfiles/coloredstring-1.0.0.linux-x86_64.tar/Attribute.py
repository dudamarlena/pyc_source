# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/coloredstring/util/Attribute.py
# Compiled at: 2016-02-29 13:04:45
from ._protected.Color import Color
__author__ = 'smt'

class Attribute(Color):
    Bold = 1
    Dim = 2
    Underlined = 4
    Blink = 5
    Reverse = 7
    Hidden = 8
    Default = 0

    @classmethod
    def get_color(cls, color_code):
        return '\x1b[' + str(color_code) + 'm'