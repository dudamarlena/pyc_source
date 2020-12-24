# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/ansi.py
# Compiled at: 2020-03-21 13:30:36
# Size of source mod 2**32: 2634 bytes
"""Module to store Ansi configurations.
In certain functions of the snakypy package, functions with named
parameters "foreground", "background" and "sgr" are found, in which you can receive a
certain foreground or background color, and font style settings in Ansi.
"""
import sys

def return_ansi_or_not(value):
    """This function checks if the operating system is Windows, and
    if an empty value is returned for each variable that represents a
    color in Ansi.

    Arguments:
        **value {str}** -- Receives a string in the form of Ansi color.

    Returns:
        **[str]** -- It will return an Ansi scape code, or an empty string.
    """
    if sys.platform.startswith('win'):
        return ''
    return value


NONE = return_ansi_or_not('\x1b[0m')

class FG:
    __doc__ = '\n    Class FG (foreground) that receives colors and ANSI settings in each of\n    the global variables below to be applied in texts.\n    '
    BLACK = return_ansi_or_not('\x1b[30m')
    MAGENTA = return_ansi_or_not('\x1b[95m')
    BLUE = return_ansi_or_not('\x1b[94m')
    GREEN = return_ansi_or_not('\x1b[92m')
    RED = return_ansi_or_not('\x1b[91m')
    YELLOW = return_ansi_or_not('\x1b[93m')
    CYAN = return_ansi_or_not('\x1b[96m')
    WHITE = return_ansi_or_not('\x1b[97m')
    WARNING = return_ansi_or_not(f"{YELLOW}⚠ ")
    ERROR = return_ansi_or_not(f"{RED}✖ ")
    FINISH = return_ansi_or_not(f"{GREEN}✔ ")
    QUESTION = return_ansi_or_not(f"{CYAN}➜ ")


class BG:
    __doc__ = '\n    Class BG (background) that receives colors and ANSI settings in each\n    of the global variables below to be applied in texts.\n    '
    BLACK = return_ansi_or_not('\x1b[40m')
    MAGENTA = return_ansi_or_not('\x1b[105m')
    BLUE = return_ansi_or_not('\x1b[104m')
    GREEN = return_ansi_or_not('\x1b[102m')
    RED = return_ansi_or_not('\x1b[101m')
    YELLOW = return_ansi_or_not('\x1b[103m')
    CYAN = return_ansi_or_not('\x1b[106m')
    WHITE = return_ansi_or_not('\x1b[107m')
    WARNING = return_ansi_or_not(f"{YELLOW}⚠ ")
    ERROR = return_ansi_or_not(f"{RED}✖ ")
    FINISH = return_ansi_or_not(f"{GREEN}✔ ")
    QUESTION = return_ansi_or_not(f"{CYAN}➜ ")


class SGR:
    __doc__ = '\n    SGR class that receives effects for text such as underline, blink, etc.\n    '
    BOLD = return_ansi_or_not('\x1b[1m')
    ITALIC = return_ansi_or_not('\x1b[3m')
    UNDERLINE = return_ansi_or_not('\x1b[4m')
    SLOW_BLINK = return_ansi_or_not('\x1b[5m')
    RAPID_BLINK = return_ansi_or_not('\x1b[6m')
    REVERSE_COLOR = return_ansi_or_not('\x1b[7m')


__all__ = [
 'NONE', 'FG', 'BG', 'SGR']