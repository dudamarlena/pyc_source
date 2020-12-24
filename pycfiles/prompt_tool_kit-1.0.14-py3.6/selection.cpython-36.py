# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/selection.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1120 bytes
"""
Data structures for the selection.
"""
from __future__ import unicode_literals
__all__ = ('SelectionType', 'PasteMode', 'SelectionState')

class SelectionType(object):
    __doc__ = '\n    Type of selection.\n    '
    CHARACTERS = 'CHARACTERS'
    LINES = 'LINES'
    BLOCK = 'BLOCK'


class PasteMode(object):
    EMACS = 'EMACS'
    VI_AFTER = 'VI_AFTER'
    VI_BEFORE = 'VI_BEFORE'


class SelectionState(object):
    __doc__ = '\n    State of the current selection.\n\n    :param original_cursor_position: int\n    :param type: :class:`~.SelectionType`\n    '

    def __init__(self, original_cursor_position=0, type=SelectionType.CHARACTERS):
        self.original_cursor_position = original_cursor_position
        self.type = type

    def __repr__(self):
        return '%s(original_cursor_position=%r, type=%r)' % (
         self.__class__.__name__,
         self.original_cursor_position, self.type)