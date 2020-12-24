# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hello52/util/log.py
# Compiled at: 2018-02-21 06:41:16
# Size of source mod 2**32: 2585 bytes
from ..version import script_name
import os, sys
TERM = os.getenv('TERM', '')
IS_ANSI_TERMINAL = TERM in ('eterm-color', 'linux', 'screen', 'vt100') or TERM.startswith('xterm')
RESET = 0
BOLD = 1
UNDERLINE = 4
NEGATIVE = 7
NO_BOLD = 21
NO_UNDERLINE = 24
POSITIVE = 27
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
LIGHT_GRAY = 37
DEFAULT = 39
BLACK_BACKGROUND = 40
RED_BACKGROUND = 41
GREEN_BACKGROUND = 42
YELLOW_BACKGROUND = 43
BLUE_BACKGROUND = 44
MAGENTA_BACKGROUND = 45
CYAN_BACKGROUND = 46
LIGHT_GRAY_BACKGROUND = 47
DEFAULT_BACKGROUND = 49
DARK_GRAY = 90
LIGHT_RED = 91
LIGHT_GREEN = 92
LIGHT_YELLOW = 93
LIGHT_BLUE = 94
LIGHT_MAGENTA = 95
LIGHT_CYAN = 96
WHITE = 97
DARK_GRAY_BACKGROUND = 100
LIGHT_RED_BACKGROUND = 101
LIGHT_GREEN_BACKGROUND = 102
LIGHT_YELLOW_BACKGROUND = 103
LIGHT_BLUE_BACKGROUND = 104
LIGHT_MAGENTA_BACKGROUND = 105
LIGHT_CYAN_BACKGROUND = 106
WHITE_BACKGROUND = 107

def sprint(text, *colors):
    """Format text with color or other effects into ANSI escaped string."""
    if IS_ANSI_TERMINAL:
        if colors:
            return '\x1b[{}m{content}\x1b[{}m'.format((';'.join([str(color) for color in colors])),
              RESET, content=text)
    return text


def println(text, *colors):
    """Print text to standard output."""
    sys.stdout.write(sprint(text, *colors) + '\n')


def print_err(text, *colors):
    """Print text to standard error."""
    sys.stderr.write(sprint(text, *colors) + '\n')


def print_log(text, *colors):
    """Print a log message to standard error."""
    sys.stderr.write(sprint('{}: {}'.format(script_name, text), *colors) + '\n')


def i(message):
    """Print a normal log message."""
    print_log(message)


def d(message):
    """Print a debug log message."""
    print_log(message, BLUE)


def w(message):
    """Print a warning log message."""
    print_log(message, YELLOW)


def e(message, exit_code=None):
    """Print an error log message."""
    print_log(message, YELLOW, BOLD)
    if exit_code is not None:
        sys.exit(exit_code)


def wtf(message, exit_code=1):
    """What a Terrible Failure!"""
    print_log(message, RED, BOLD)
    if exit_code is not None:
        sys.exit(exit_code)