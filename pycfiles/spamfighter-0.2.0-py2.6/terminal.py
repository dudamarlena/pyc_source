# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/utils/terminal.py
# Compiled at: 2009-02-17 05:43:07
"""
Terminal controller module.

Example of usage:
print BG_BLUE + 'Text on blue background' + NORMAL
print BLUE + UNDERLINE + 'Blue underlined text' + NORMAL
print BLUE + BG_YELLOW + BOLD + 'text' + NORMAL
"""
import sys
MODULE = sys.modules[__name__]
COLORS = ('BLUE GREEN CYAN RED MAGENTA YELLOW WHITE BLACK').split()
CONTROLS = {'BOL': 'cr', 
   'UP': 'cuu1', 'DOWN': 'cud1', 'LEFT': 'cub1', 'RIGHT': 'cuf1', 'CLEAR_SCREEN': 'clear', 
   'CLEAR_EOL': 'el', 'CLEAR_BOL': 'el1', 'CLEAR_EOS': 'ed', 
   'BOLD': 'bold', 'BLINK': 'blink', 'DIM': 'dim', 'REVERSE': 'rev', 
   'UNDERLINE': 'smul', 'NORMAL': 'sgr0', 'HIDE_CURSOR': 'cinvis', 
   'SHOW_CURSOR': 'cnorm'}
VALUES = {'COLUMNS': 'cols', 
   'LINES': 'lines', 
   'MAX_COLORS': 'colors'}

def default():
    """Set the default attribute values"""
    for color in COLORS:
        setattr(MODULE, color, '')
        setattr(MODULE, 'BG_%s' % color, '')

    for control in CONTROLS:
        setattr(MODULE, control, '')

    for value in VALUES:
        setattr(MODULE, value, None)

    return


def setup():
    """Set the terminal control strings"""
    curses.setupterm()
    bgColorSeq = curses.tigetstr('setab') or curses.tigetstr('setb') or ''
    fgColorSeq = curses.tigetstr('setaf') or curses.tigetstr('setf') or ''
    for color in COLORS:
        colorIndex = getattr(curses, 'COLOR_%s' % color)
        setattr(MODULE, color, curses.tparm(fgColorSeq, colorIndex))
        setattr(MODULE, 'BG_%s' % color, curses.tparm(bgColorSeq, colorIndex))

    for control in CONTROLS:
        setattr(MODULE, control, curses.tigetstr(CONTROLS[control]) or '')

    for value in VALUES:
        setattr(MODULE, value, curses.tigetnum(VALUES[value]))


def render(text):
    """Helper function to apply controls easily.
    Example:
    apply("%(GREEN)s%(BOLD)stext%(NORMAL)s") -> a bold green text
    """
    return text % MODULE.__dict__


try:
    import curses
    setup()
except Exception, e:
    print 'Warning: %s' % e
    default()