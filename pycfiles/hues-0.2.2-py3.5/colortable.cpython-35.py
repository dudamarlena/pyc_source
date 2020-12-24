# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hues/colortable.py
# Compiled at: 2016-10-02 07:50:59
# Size of source mod 2**32: 1130 bytes
"""Generate ANSI escape sequences for colors
Source: http://ascii-table.com/ansi-escape-sequences.php
"""
from collections import namedtuple
ANSIColors = namedtuple('ANSIColors', [
 'black', 'red', 'green', 'yellow',
 'blue', 'magenta', 'cyan', 'white'])
ANSIStyles = namedtuple('ANSIStyles', [
 'reset', 'bold', 'italic', 'underline', 'defaultfg', 'defaultbg'])
STYLE = ANSIStyles(0, 1, 3, 4, 39, 49)
FG = ANSIColors(*range(30, 38))
BG = ANSIColors(*range(40, 48))
HI_FG = ANSIColors(*range(90, 98))
HI_BG = ANSIColors(*range(100, 108))
SEQ = '\x1b[%sm'

def __gen_keywords__(*args, **kwargs):
    """Helper function to generate single escape sequence mapping."""
    fields = tuple()
    values = tuple()
    for tpl in args:
        fields += tpl._fields
        values += tpl

    for prefix, tpl in kwargs.items():
        fields += tuple(map(lambda x: '_'.join([prefix, x]), tpl._fields))
        values += tpl

    return namedtuple('ANSISequences', fields)(*values)


KEYWORDS = __gen_keywords__(STYLE, FG, bg=BG, bright=HI_FG, bg_bright=HI_BG)