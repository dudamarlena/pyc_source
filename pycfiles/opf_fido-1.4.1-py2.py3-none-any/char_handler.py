# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fido/char_handler.py
# Compiled at: 2019-10-29 14:38:34
"""Character handling routines for Format Identification for Digital Objects (FIDO)."""
ORDINARY = frozenset(' "#%&\',-/0123456789:;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~')
SPECIAL = '$()*+.?![]^\\{|}'
HEX = '0123456789abcdef'

def escape_char(c):
    """Add appropriate escape sequence to passed character c."""
    if c in '\n':
        return '\\n'
    if c == '\r':
        return '\\r'
    if c in SPECIAL:
        return '\\' + c
    high, low = divmod(ord(c), 16)
    return '\\x' + HEX[high] + HEX[low]


def escape(string):
    """Escape characters in pattern that are non-printable, non-ascii, or special for regexes."""
    return ('').join((c if c in ORDINARY else escape_char(c)) for c in string)