# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/key_binding/vi_state.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1734 bytes
from __future__ import unicode_literals
__all__ = ('InputMode', 'CharacterFind', 'ViState')

class InputMode(object):
    INSERT = 'vi-insert'
    INSERT_MULTIPLE = 'vi-insert-multiple'
    NAVIGATION = 'vi-navigation'
    REPLACE = 'vi-replace'


class CharacterFind(object):

    def __init__(self, character, backwards=False):
        self.character = character
        self.backwards = backwards


class ViState(object):
    """ViState"""

    def __init__(self):
        self.last_character_find = None
        self.operator_func = None
        self.operator_arg = None
        self.named_registers = {}
        self.input_mode = InputMode.INSERT
        self.waiting_for_digraph = False
        self.digraph_symbol1 = None
        self.tilde_operator = False

    def reset(self, mode=InputMode.INSERT):
        """
        Reset state, go back to the given mode. INSERT by default.
        """
        self.input_mode = mode
        self.waiting_for_digraph = False
        self.operator_func = None
        self.operator_arg = None