# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/colorama/ansi.py
# Compiled at: 2018-11-28 03:20:09
"""
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
"""
CSI = '\x1b['

def code_to_chars(code):
    return CSI + str(code) + 'm'


class AnsiCodes(object):

    def __init__(self, codes):
        for name in dir(codes):
            if not name.startswith('_'):
                value = getattr(codes, name)
                setattr(self, name, code_to_chars(value))


class AnsiFore:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39


class AnsiBack:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49


class AnsiStyle:
    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    RESET_ALL = 0


Fore = AnsiCodes(AnsiFore)
Back = AnsiCodes(AnsiBack)
Style = AnsiCodes(AnsiStyle)