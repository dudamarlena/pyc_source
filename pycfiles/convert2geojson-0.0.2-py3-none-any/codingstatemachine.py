# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/codingstatemachine.py
# Compiled at: 2018-01-22 17:51:30
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