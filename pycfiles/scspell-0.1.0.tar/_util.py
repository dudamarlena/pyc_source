# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paul/src/scspell-0.1/scspell_lib/_util.py
# Compiled at: 2009-06-06 00:05:46
"""
_util -- utility functions which may be useful across the source tree.
"""
VERBOSITY_NORMAL = 1
VERBOSITY_DEBUG = 2
VERBOSITY_MAX = VERBOSITY_DEBUG
SETTINGS = {'verbosity': VERBOSITY_NORMAL}

def mutter(level, text):
    """Print text to the console, if the level is not higher than the
    current verbosity setting."""
    if level <= SETTINGS['verbosity']:
        print text


def set_verbosity(value):
    """Set the verbosity level to a given integral value.  The constants
    VERBOSITY_* are good choices."""
    SETTINGS['verbosity'] = value