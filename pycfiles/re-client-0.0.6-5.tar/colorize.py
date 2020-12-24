# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbielawa/rhat/release-engine/re-client/src/reclient/colorize.py
# Compiled at: 2014-05-21 16:38:44
BG = {}
BG['BLACK'] = '\x1b[40m'
BG['RED'] = '\x1b[41m'
BG['GREEN'] = '\x1b[42m'
BG['YELLOW'] = '\x1b[43m'
BG['BLUE'] = '\x1b[44m'
BG['PURPLE'] = '\x1b[45m'
BG['CYAN'] = '\x1b[46m'
BG['LIGHTGRAY'] = '\x1b[47m'
COLORS = {}
COLORS['RESTORE'] = '\x1b[0m'
COLORS['RED'] = '\x1b[00;31m'
COLORS['GREEN'] = '\x1b[00;32m'
COLORS['YELLOW'] = '\x1b[00;33m'
COLORS['BLUE'] = '\x1b[00;34m'
COLORS['PURPLE'] = '\x1b[00;35m'
COLORS['CYAN'] = '\x1b[00;36m'
COLORS['TEAL'] = '\x1b[00;36m'
COLORS['LIGHTGRAY'] = '\x1b[00;37m'
COLORS['LRED'] = '\x1b[01;31m'
COLORS['LGREEN'] = '\x1b[01;32m'
COLORS['LYELLOW'] = '\x1b[01;33m'
COLORS['LBLUE'] = '\x1b[01;34m'
COLORS['LPURPLE'] = '\x1b[01;35m'
COLORS['LCYAN'] = '\x1b[01;36m'
COLORS['WHITE'] = '\x1b[01;37m'

def colorize(item, color=None, underline=False, background=None):
    if underline:
        ul = '\x1b[4m'
    else:
        ul = ''
    if background:
        bg = BG[background.upper()]
    else:
        bg = ''
    if color:
        c = COLORS[color.upper()]
    else:
        c = COLORS['WHITE']
    return '%s%s%s%s%s%s' % (COLORS['RESTORE'],
     c,
     bg, ul, item,
     COLORS['RESTORE'])