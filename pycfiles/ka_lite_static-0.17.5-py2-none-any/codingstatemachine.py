# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/requests/requests/packages/chardet/codingstatemachine.py
# Compiled at: 2018-07-11 18:15:32
from .constants import eStart
from .compat import wrap_ord

class CodingStateMachine:

    def __init__(self, sm):
        self._mModel = sm
        self._mCurrentBytePos = 0
        self._mCurrentCharLen = 0
        self.reset()

    def reset(self):
        self._mCurrentState = eStart

    def next_state(self, c):
        byteCls = self._mModel['classTable'][wrap_ord(c)]
        if self._mCurrentState == eStart:
            self._mCurrentBytePos = 0
            self._mCurrentCharLen = self._mModel['charLenTable'][byteCls]
        curr_state = self._mCurrentState * self._mModel['classFactor'] + byteCls
        self._mCurrentState = self._mModel['stateTable'][curr_state]
        self._mCurrentBytePos += 1
        return self._mCurrentState

    def get_current_charlen(self):
        return self._mCurrentCharLen

    def get_coding_state_machine(self):
        return self._mModel['name']