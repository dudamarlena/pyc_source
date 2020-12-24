# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/selection.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1120 bytes
__doc__ = '\nData structures for the selection.\n'
from __future__ import unicode_literals
__all__ = ('SelectionType', 'PasteMode', 'SelectionState')

class SelectionType(object):
    """SelectionType"""
    CHARACTERS = 'CHARACTERS'
    LINES = 'LINES'
    BLOCK = 'BLOCK'


class PasteMode(object):
    EMACS = 'EMACS'
    VI_AFTER = 'VI_AFTER'
    VI_BEFORE = 'VI_BEFORE'


class SelectionState(object):
    """SelectionState"""

    def __init__(self, original_cursor_position=0, type=SelectionType.CHARACTERS):
        self.original_cursor_position = original_cursor_position
        self.type = type

    def __repr__(self):
        return '%s(original_cursor_position=%r, type=%r)' % (
         self.__class__.__name__,
         self.original_cursor_position, self.type)