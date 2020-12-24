# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fragments/color.py
# Compiled at: 2012-11-13 05:59:16
from __future__ import unicode_literals
import os, sys
GREY = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37
BRIGHT_WHITE = 57
NORMAL = 0
BOLD = 1

class ColoredString(type(b'')):
    color = WHITE
    weight = NORMAL

    def colorize(self):
        if sys.stdout.isatty():
            return b'\x1b[%sm\x1b[%sm%s\x1b[0m' % (self.weight, self.color, self)
        else:
            return self


class Added(ColoredString):

    @property
    def color(self):
        if os.getenv(b'COLORBLIND', b'').lower() in ('protan', 'deutan'):
            return BLUE
        return GREEN


class Deleted(ColoredString):
    color = RED


class Modified(ColoredString):
    color = YELLOW


class LineNumber(ColoredString):
    color = MAGENTA


class Unknown(ColoredString):
    color = MAGENTA


class Error(ColoredString):
    color = GREY


class DeletedHeader(Deleted):
    weight = BOLD


class AddedHeader(Added):
    weight = BOLD


class Header(ColoredString):
    color = BRIGHT_WHITE
    weight = BOLD


class Prompt(ColoredString):
    color = YELLOW
    weight = BOLD

    def __new__(cls, s):
        return super(Prompt, cls).__new__(cls, s + b' ')