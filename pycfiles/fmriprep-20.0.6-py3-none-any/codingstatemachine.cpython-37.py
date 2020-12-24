# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/chardet/codingstatemachine.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 3590 bytes
import logging
from .enums import MachineState

class CodingStateMachine(object):
    __doc__ = '\n    A state machine to verify a byte sequence for a particular encoding. For\n    each byte the detector receives, it will feed that byte to every active\n    state machine available, one byte at a time. The state machine changes its\n    state based on its previous state and the byte it receives. There are 3\n    states in a state machine that are of interest to an auto-detector:\n\n    START state: This is the state to start with, or a legal byte sequence\n                 (i.e. a valid code point) for character has been identified.\n\n    ME state:  This indicates that the state machine identified a byte sequence\n               that is specific to the charset it is designed for and that\n               there is no other possible encoding which can contain this byte\n               sequence. This will to lead to an immediate positive answer for\n               the detector.\n\n    ERROR state: This indicates the state machine identified an illegal byte\n                 sequence for that encoding. This will lead to an immediate\n                 negative answer for this encoding. Detector will exclude this\n                 encoding from consideration from here on.\n    '

    def __init__(self, sm):
        self._model = sm
        self._curr_byte_pos = 0
        self._curr_char_len = 0
        self._curr_state = None
        self.logger = logging.getLogger(__name__)
        self.reset()

    def reset(self):
        self._curr_state = MachineState.START

    def next_state(self, c):
        byte_class = self._model['class_table'][c]
        if self._curr_state == MachineState.START:
            self._curr_byte_pos = 0
            self._curr_char_len = self._model['char_len_table'][byte_class]
        curr_state = self._curr_state * self._model['class_factor'] + byte_class
        self._curr_state = self._model['state_table'][curr_state]
        self._curr_byte_pos += 1
        return self._curr_state

    def get_current_charlen(self):
        return self._curr_char_len

    def get_coding_state_machine(self):
        return self._model['name']

    @property
    def language(self):
        return self._model['language']