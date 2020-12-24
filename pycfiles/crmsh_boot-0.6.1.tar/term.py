# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/term.py
# Compiled at: 2016-05-04 07:56:27
import sys, re

class colors(object):
    BOL = ''
    UP = ''
    DOWN = ''
    LEFT = ''
    RIGHT = ''
    CLEAR_SCREEN = ''
    CLEAR_EOL = ''
    CLEAR_BOL = ''
    CLEAR_EOS = ''
    BOLD = ''
    BLINK = ''
    DIM = ''
    REVERSE = ''
    UNDERLINE = ''
    NORMAL = ''
    HIDE_CURSOR = ''
    SHOW_CURSOR = ''
    COLS = None
    LINES = None
    BLACK = BLUE = GREEN = CYAN = RED = MAGENTA = YELLOW = WHITE = ''
    BG_BLACK = BG_BLUE = BG_GREEN = BG_CYAN = ''
    BG_RED = BG_MAGENTA = BG_YELLOW = BG_WHITE = ''
    RLIGNOREBEGIN = '\x01'
    RLIGNOREEND = '\x02'


_STRING_CAPABILITIES = ('\nBOL=cr UP=cuu1 DOWN=cud1 LEFT=cub1 RIGHT=cuf1\nCLEAR_SCREEN=clear CLEAR_EOL=el CLEAR_BOL=el1 CLEAR_EOS=ed BOLD=bold\nBLINK=blink DIM=dim REVERSE=rev UNDERLINE=smul NORMAL=sgr0\nHIDE_CURSOR=cinvis SHOW_CURSOR=cnorm').split()
_COLORS = ('BLACK BLUE GREEN CYAN RED MAGENTA YELLOW WHITE').split()
_ANSICOLORS = ('BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE').split()

def init():
    """
    Initialize attributes with appropriate values for the current terminal.

    `_term_stream` is the stream that will be used for terminal
    output; if this stream is not a tty, then the terminal is
    assumed to be a dumb terminal (i.e., have no capabilities).
    """

    def _tigetstr(cap_name):
        import curses
        cap = curses.tigetstr(cap_name) or ''
        cap = re.sub('\\$<\\d+>[*]?', '', cap)
        if cap_name == 'sgr0':
            cap = re.sub('\\017$', '', cap)
        return cap

    _term_stream = sys.stdout
    try:
        import curses
    except:
        sys.stderr.write("INFO: no curses support: you won't see colors\n")
        return

    from . import config
    if not _term_stream.isatty() and 'color-always' not in config.color.style:
        return
    try:
        curses.setupterm()
    except:
        return

    colors.COLS = curses.tigetnum('cols')
    colors.LINES = curses.tigetnum('lines')
    for capability in _STRING_CAPABILITIES:
        attrib, cap_name = capability.split('=')
        setattr(colors, attrib, _tigetstr(cap_name) or '')

    set_fg = _tigetstr('setf')
    if set_fg:
        for i, color in zip(range(len(_COLORS)), _COLORS):
            setattr(colors, color, curses.tparm(set_fg, i) or '')

    set_fg_ansi = _tigetstr('setaf')
    if set_fg_ansi:
        for i, color in zip(range(len(_ANSICOLORS)), _ANSICOLORS):
            setattr(colors, color, curses.tparm(set_fg_ansi, i) or '')

    set_bg = _tigetstr('setb')
    if set_bg:
        for i, color in zip(range(len(_COLORS)), _COLORS):
            setattr(colors, 'BG_' + color, curses.tparm(set_bg, i) or '')

    set_bg_ansi = _tigetstr('setab')
    if set_bg_ansi:
        for i, color in zip(range(len(_ANSICOLORS)), _ANSICOLORS):
            setattr(colors, 'BG_' + color, curses.tparm(set_bg_ansi, i) or '')


def render(template):
    """
    Replace each $-substitutions in the given template string with
    the corresponding terminal control string (if it's defined) or
    '' (if it's not).
    """

    def render_sub(match):
        s = match.group()
        return getattr(colors, s[2:-1].upper(), '')

    return re.sub('\\${\\w+}', render_sub, template)


def is_color(s):
    return hasattr(colors, s.upper())