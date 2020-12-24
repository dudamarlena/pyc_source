# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sblibs/display/color.py
# Compiled at: 2017-09-18 18:37:05
"""
    Module focused in termcolor operations

    If the exection is not attatched in any tty,
    so colored is disabled
"""
from __future__ import unicode_literals
import sys
COLORED = True
if not sys.stdout.isatty() or sys.platform == b'win32':
    COLORED = False
COLOR_MAP = {b'brown': b'\x1b[{style};30m', 
   b'red': b'\x1b[{style};31m', 
   b'green': b'\x1b[{style};32m', 
   b'yellow': b'\x1b[{style};33m', 
   b'blue': b'\x1b[{style};34m', 
   b'pink': b'\x1b[{style};35m', 
   b'cyan': b'\x1b[{style};36m', 
   b'gray': b'\x1b[{style};37m', 
   b'white': b'\x1b[{style};40m', 
   b'reset': b'\x1b[00;00m'}
STYLE_MAP = {b'normal': b'00', 
   b'bold': b'01', 
   b'underline': b'04'}

def colorize(printable, color, style=b'normal', autoreset=True):
    """Colorize some message with ANSI colors specification

    :param printable: interface whose has __str__ or __repr__ method
    :param color: the colors defined in COLOR_MAP to colorize the text
    :style: can be 'normal', 'bold' or 'underline'

    :returns: the 'printable' colorized with style
    """
    if not COLORED:
        return printable
    if color not in COLOR_MAP:
        raise RuntimeError((b'invalid color set, no {}').format(color))
    return (b'{color}{printable}{reset}').format(printable=printable, color=COLOR_MAP[color].format(style=STYLE_MAP[style]), reset=COLOR_MAP[b'reset'] if autoreset else b'')