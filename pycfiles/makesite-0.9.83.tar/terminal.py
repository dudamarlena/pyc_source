# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klen/Projects/makesite/makesite/terminal.py
# Compiled at: 2012-09-05 10:32:55
import sys
_ESCAPE_SEQUENCE_PATTERN = '\x1b[%sm'
_ESCAPE_SEQUENCE_SEPARATOR = ';'
_BACKGROUND_COLOR = '4'
_FOREGROUND_COLOR = '3'
BLACK = '0'
RED = '1'
GREEN = '2'
BROWN = '3'
BLUE = '4'
MAGENTA = '5'
CYAN = '6'
GREY = '7'
COLOR_DEFAULT = '9'
RESET_TEXT_ATTRIBUTES = '0'
BOLD = '1'
ITALIC = '2'
UNDERLINE = '4'
COLORIZE = sys.stdout.isatty()

def bg(color):
    return _BACKGROUND_COLOR + str(int(color))


def fg(color):
    return _FOREGROUND_COLOR + str(int(color))


def styled_text(text, *style_attributes):
    if not COLORIZE:
        return text
    return '%s%s%s' % (
     _ESCAPE_SEQUENCE_PATTERN % _ESCAPE_SEQUENCE_SEPARATOR.join(style_attributes),
     text,
     _ESCAPE_SEQUENCE_PATTERN % '0;0')


def bold(text):
    return styled_text(text, BOLD)


def italic(text):
    return styled_text(text, ITALIC)


def underline(text):
    return styled_text(text, UNDERLINE)