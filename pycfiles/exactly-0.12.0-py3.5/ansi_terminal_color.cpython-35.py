# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/ansi_terminal_color.py
# Compiled at: 2020-01-23 16:48:01
# Size of source mod 2**32: 917 bytes
import os
from enum import IntEnum

class ForegroundColor(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92


class FontStyle(IntEnum):
    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4


def ansi_escape(foreground: ForegroundColor, s: str) -> str:
    return '\x1b[1;' + str(int(foreground)) + 'm' + s + '\x1b[1;m'


def set_color(foreground: ForegroundColor) -> str:
    return '\x1b[1;' + str(int(foreground)) + 'm'


def set_font_style(style: FontStyle) -> str:
    return '\x1b[1;' + str(int(style)) + 'm'


def unset_color() -> str:
    return '\x1b[1;m'


def unset_font_style() -> str:
    return '\x1b[1;0m'


def is_file_object_with_color(file_object) -> bool:
    try:
        os.ttyname(file_object.fileno())
        return True
    except (AttributeError, OSError):
        return False