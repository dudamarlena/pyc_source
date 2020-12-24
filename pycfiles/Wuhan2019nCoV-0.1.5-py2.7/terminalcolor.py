# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wuhanncov/terminalcolor.py
# Compiled at: 2020-01-22 11:05:54
RESET = '\x1b[0m'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def termcolor(fg=None, bg=None):
    codes = []
    if fg is not None:
        codes.append('3%d' % fg)
    if bg is not None:
        codes.append('10%d' % bg)
    if codes:
        return '\x1b[%sm' % (';').join(codes)
    else:
        return ''


def colorize(message, fg=None, bg=None):
    if fg is None:
        if bg == BLACK:
            fg = WHITE
        else:
            fg = BLACK
    return termcolor(fg, bg) + message + RESET