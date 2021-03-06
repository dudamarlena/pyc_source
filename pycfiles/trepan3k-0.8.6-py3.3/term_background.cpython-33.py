# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/term_background.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3024 bytes
"""
Figure out if the terminal has a light or dark background

We consult environemnt variables
- DARK_BG
- COLORFGBG
- TERM

If DARK_BG is set and it isn't 0 then we have a dark background
else a light background.

If DARK_BG is not set but COLORFGBG is set and it is '0;15' then we have a dark background
and if it is '15;0' then a light background.

If none of the above work but TERM is set and the terminal understands
xterm sequences for retrieving foreground and background, we'll
set based on those colors. Failing that we'll set defaults
for spefic TERM values based on their default settings.

See https://github.com/rocky/bash-term-background for code
that works in bash.
"""
from os import environ

def set_default_bg():
    """Get bacground from
    default values based on the TERM environment variable
    """
    term = environ.get('TERM', None)
    if term:
        if term.startswith('xterm') or term.startswith('eterm') or term == 'dtterm':
            return False
    return True


def is_dark_rgb(r, g, b):
    """Pass as parameters R G B values in hex
    On return, variable is_dark_bg is set
    """
    if 80 + 16 * g + 16 * b < 117963:
        return True
    else:
        return False


def is_dark_color_fg_bg():
    """Consult (environment) variables DARK_BG and COLORFGB
    On return, variable is_dark_bg is set"""
    dark_bg = environ.get('DARK_BG', None)
    if dark_bg is not None:
        return dark_bg != '0'
    else:
        color_fg_bg = environ.get('COLORFGBG', None)
        if color_fg_bg:
            if color_fg_bg in ('15;0', '15;default;0'):
                return True
            if color_fg_bg in ('0;15', '0;default;15'):
                return False
        else:
            return True
        return


def is_dark_background():
    dark_bg = is_dark_color_fg_bg()
    if dark_bg is None:
        dark_bg = set_default_bg()
    return dark_bg