# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/apps/console/color.py
# Compiled at: 2013-02-01 06:44:08
import curses
_BACKGROUND = -1

def init():
    global BG_GREEN
    global BG_MAGENTA
    global BLUE
    global DEFAULT
    global GREEN
    curses.use_default_colors()
    DEFAULT = curses.color_pair(0)
    curses.init_pair(1, curses.COLOR_BLUE, _BACKGROUND)
    BLUE = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_GREEN, _BACKGROUND)
    GREEN = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    BG_MAGENTA = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    BG_GREEN = curses.color_pair(4)