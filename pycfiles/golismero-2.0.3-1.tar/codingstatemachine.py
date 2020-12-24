# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/codingstatemachine.py
# Compiled at: 2013-12-09 06:41:17
from constants import eStart, eError, eItsMe

class CodingStateMachine:

    def __init__(self, sm):
        self._mModel = sm
        self._mCurrentBytePos = 0
        self._mCurrentCharLen = 0
        self.reset()

    def reset(self):
        self._mCurrentState = eStart

    def next_state(self, c):
        byteCls = self._mModel['classTable'][ord(c)]
        if self._mCurrentState == eStart:
            self._mCurrentBytePos = 0
            self._mCurrentCharLen = self._mModel['charLenTable'][byteCls]
        self._mCurrentState = self._mModel['stateTable'][(self._mCurrentState * self._mModel['classFactor'] + byteCls)]
        self._mCurrentBytePos += 1
        return self._mCurrentState

    def get_current_charlen(self):
        return self._mCurrentCharLen

    def get_coding_state_machine(self):
        return self._mModel['name']