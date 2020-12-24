# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/screen.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 4484 bytes
from __future__ import unicode_literals
from prompt_tool_kit.cache import FastDictCache
from prompt_tool_kit.token import Token
from prompt_tool_kit.utils import get_cwidth
from collections import defaultdict, namedtuple
__all__ = ('Point', 'Size', 'Screen', 'Char')
Point = namedtuple('Point', 'y x')
Size = namedtuple('Size', 'rows columns')

class Char(object):
    """Char"""
    __slots__ = ('char', 'token', 'width')
    display_mappings = {'\x00':'^@', 
     '\x01':'^A', 
     '\x02':'^B', 
     '\x03':'^C', 
     '\x04':'^D', 
     '\x05':'^E', 
     '\x06':'^F', 
     '\x07':'^G', 
     '\x08':'^H', 
     '\t':'^I', 
     '\n':'^J', 
     '\x0b':'^K', 
     '\x0c':'^L', 
     '\r':'^M', 
     '\x0e':'^N', 
     '\x0f':'^O', 
     '\x10':'^P', 
     '\x11':'^Q', 
     '\x12':'^R', 
     '\x13':'^S', 
     '\x14':'^T', 
     '\x15':'^U', 
     '\x16':'^V', 
     '\x17':'^W', 
     '\x18':'^X', 
     '\x19':'^Y', 
     '\x1a':'^Z', 
     '\x1b':'^[', 
     '\x1c':'^\\', 
     '\x1d':'^]', 
     '\x1f':'^_', 
     '\x7f':'^?'}

    def __init__(self, char=' ', token=Token):
        char = self.display_mappings.get(char, char)
        self.char = char
        self.token = token
        self.width = get_cwidth(char)

    def __eq__(self, other):
        return self.char == other.char and self.token == other.token

    def __ne__(self, other):
        return self.char != other.char or self.token != other.token

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.char, self.token)


_CHAR_CACHE = FastDictCache(Char, size=1000000)
Transparent = Token.Transparent

class Screen(object):
    """Screen"""

    def __init__(self, default_char=None, initial_width=0, initial_height=0):
        if default_char is None:
            default_char = _CHAR_CACHE[(' ', Transparent)]
        self.data_buffer = defaultdict(lambda : defaultdict(lambda : default_char))
        self.zero_width_escapes = defaultdict(lambda : defaultdict(lambda : ''))
        self.cursor_position = Point(y=0, x=0)
        self.show_cursor = True
        self.menu_position = None
        self.width = initial_width or 0
        self.height = initial_height or 0

    def replace_all_tokens(self, token):
        """
        For all the characters in the screen. Set the token to the given `token`.
        """
        b = self.data_buffer
        for y, row in b.items():
            for x, char in row.items():
                b[y][x] = _CHAR_CACHE[(char.char, token)]


class WritePosition(object):

    def __init__(self, xpos, ypos, width, height, extended_height=None):
        if not height >= 0:
            raise AssertionError
        else:
            if not extended_height is None:
                if not extended_height >= 0:
                    raise AssertionError
            assert width >= 0
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.extended_height = extended_height or height

    def __repr__(self):
        return '%s(%r, %r, %r, %r, %r)' % (
         self.__class__.__name__,
         self.xpos, self.ypos, self.width, self.height, self.extended_height)