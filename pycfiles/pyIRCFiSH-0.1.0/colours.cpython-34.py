# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/formatting/colours.py
# Compiled at: 2015-10-08 05:15:48
# Size of source mod 2**32: 3901 bytes
__doc__ = 'Colour codes for IRC messages.\n\nThis module contains the constants for IRC colour codes, including RGB and ANSI\nescape translations of them.\n\n'
try:
    from enum import Enum, IntEnum, unique
except ImportError:
    from PyIRC.util.enum import Enum, IntEnum, unique

from collections import namedtuple

class ColourRGB(namedtuple('ColourRGB', 'red green blue')):
    """ColourRGB"""

    @property
    def html(self):
        """Convert triplet to HTML format."""
        return '#{:02X}{:02X}{:02X}'.format(self.red, self.green, self.blue)


class ColourEscape(namedtuple('ColourEscape', 'intense base')):
    """ColourEscape"""

    @property
    def foreground(self):
        """The ANSI constant for the foreground variant of this colour."""
        return self.base + 30

    @property
    def background(self):
        """The ANSI constant for the background variant of this colour."""
        return self.base + 40

    @property
    def foreground_16(self):
        """The XTerm constant for the foreground variant of this colour in
        16-colour mode."""
        return self.foreground + 60 * self.intense

    @property
    def background_16(self):
        """The XTerm constant for the background variant of this colour in
        16-colour mode."""
        return self.background + 60 * self.intense


@unique
class Colours(IntEnum):
    """Colours"""
    white = 0
    black = 1
    blue = 2
    green = 3
    light_red = 4
    brown = 5
    purple = 6
    orange = 7
    yellow = 8
    light_green = 9
    cyan = 10
    light_cyan = 11
    light_blue = 12
    pink = 13
    grey = 14
    light_grey = 15


@unique
class ColoursRGB(Enum):
    """ColoursRGB"""
    white = ColourRGB(255, 255, 255)
    black = ColourRGB(0, 0, 0)
    blue = ColourRGB(0, 0, 127)
    green = ColourRGB(0, 147, 0)
    light_red = ColourRGB(255, 0, 0)
    brown = ColourRGB(127, 0, 0)
    purple = ColourRGB(156, 0, 156)
    orange = ColourRGB(252, 127, 0)
    yellow = ColourRGB(255, 255, 0)
    light_green = ColourRGB(0, 252, 0)
    cyan = ColourRGB(0, 147, 147)
    light_cyan = ColourRGB(0, 255, 255)
    light_blue = ColourRGB(0, 0, 252)
    pink = ColourRGB(255, 0, 255)
    grey = ColourRGB(127, 127, 127)
    light_grey = ColourRGB(210, 210, 210)


@unique
class ColoursANSI(Enum):
    """ColoursANSI"""
    white = ColourEscape(True, 7)
    black = ColourEscape(False, 0)
    blue = ColourEscape(False, 4)
    green = ColourEscape(False, 2)
    light_red = ColourEscape(True, 1)
    brown = ColourEscape(False, 1)
    purple = ColourEscape(False, 5)
    orange = ColourEscape(False, 3)
    yellow = ColourEscape(True, 3)
    light_green = ColourEscape(True, 2)
    cyan = ColourEscape(False, 6)
    light_cyan = ColourEscape(True, 6)
    light_blue = ColourEscape(True, 4)
    pink = ColourEscape(True, 5)
    grey = ColourEscape(True, 0)
    light_grey = ColourEscape(False, 7)


@unique
class ColoursXTerm256(Enum):
    """ColoursXTerm256"""
    white = 15
    black = 0
    blue = 4
    green = 28
    light_red = 9
    brown = 1
    purple = 127
    orange = 208
    yellow = 11
    light_green = 10
    cyan = 30
    light_cyan = 14
    light_blue = 12
    pink = 13
    grey = 8
    light_grey = 252