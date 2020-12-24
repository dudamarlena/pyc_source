# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asciicanvas/style.py
# Compiled at: 2017-11-06 15:51:10


class Style(object):
    """
    Style for canvas elements
    """

    def __init__(self, char=None, fg_color=None, bg_color=None, font_style=0):
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font_style = font_style