# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/escprober.py
# Compiled at: 2018-01-22 17:51:30
from . import constants
from .escsm import HZSMModel, ISO2022CNSMModel, ISO2022JPSMModel, ISO2022KRSMModel
from .charsetprober import CharSetProber
from .codingstatemachine import CodingStateMachine
from .compat import wrap_ord

class EscCharSetProber(CharSetProber):

    def __init__(self):
        CharSetProber.__init__(self)
        self._mCodingSM = [
         CodingStateMachine(HZSMModel),
         CodingStateMachine(ISO2022CNSMModel),
         CodingStateMachine(ISO2022JPSMModel),
         CodingStateMachine(ISO2022KRSMModel)]
        self.reset()

    def reset(self):
        CharSetProber.reset(self)
        for codingSM in self._mCodingSM:
            if not codingSM:
                continue
            codingSM.active = True
            codingSM.reset()

        self._mActiveSM = len(self._mCodingSM)
        self._mDetectedCharset = None
        return

    def get_charset_name(self):
        return self._mDetectedCharset

    def get_confidence(self):
        if self._mDetectedCharset:
            return 0.99
        else:
            return 0.0

    def feed(self, aBuf):
        for c in aBuf:
            for codingSM in self._mCodingSM:
                if not codingSM:
                    continue
                if not codingSM.active:
                    continue
                codingState = codingSM.next_state(wrap_ord(c))
                if codingState == constants.eError:
                    codingSM.active = False
                    self._mActiveSM -= 1
                    if self._mActiveSM <= 0:
                        self._mState = constants.eNotMe
                        return self.get_state()
                elif codingState == constants.eItsMe:
                    self._mState = constants.eFoundIt
                    self._mDetectedCharset = codingSM.get_coding_state_machine()
                    return self.get_state()

        return self.get_state()