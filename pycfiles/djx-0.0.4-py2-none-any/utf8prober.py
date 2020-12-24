# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/chardet/utf8prober.py
# Compiled at: 2019-02-14 00:35:06
from .charsetprober import CharSetProber
from .enums import ProbingState, MachineState
from .codingstatemachine import CodingStateMachine
from .mbcssm import UTF8_SM_MODEL

class UTF8Prober(CharSetProber):
    ONE_CHAR_PROB = 0.5

    def __init__(self):
        super(UTF8Prober, self).__init__()
        self.coding_sm = CodingStateMachine(UTF8_SM_MODEL)
        self._num_mb_chars = None
        self.reset()
        return

    def reset(self):
        super(UTF8Prober, self).reset()
        self.coding_sm.reset()
        self._num_mb_chars = 0

    @property
    def charset_name(self):
        return 'utf-8'

    @property
    def language(self):
        return ''

    def feed(self, byte_str):
        for c in byte_str:
            coding_state = self.coding_sm.next_state(c)
            if coding_state == MachineState.ERROR:
                self._state = ProbingState.NOT_ME
                break
            elif coding_state == MachineState.ITS_ME:
                self._state = ProbingState.FOUND_IT
                break
            elif coding_state == MachineState.START:
                if self.coding_sm.get_current_charlen() >= 2:
                    self._num_mb_chars += 1

        if self.state == ProbingState.DETECTING:
            if self.get_confidence() > self.SHORTCUT_THRESHOLD:
                self._state = ProbingState.FOUND_IT
        return self.state

    def get_confidence(self):
        unlike = 0.99
        if self._num_mb_chars < 6:
            unlike *= self.ONE_CHAR_PROB ** self._num_mb_chars
            return 1.0 - unlike
        else:
            return unlike