# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/utf8prober.py
# Compiled at: 2013-12-09 06:41:17
import constants, sys
from constants import eStart, eError, eItsMe
from charsetprober import CharSetProber
from codingstatemachine import CodingStateMachine
from mbcssm import UTF8SMModel
ONE_CHAR_PROB = 0.5

class UTF8Prober(CharSetProber):

    def __init__(self):
        CharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(UTF8SMModel)
        self.reset()

    def reset(self):
        CharSetProber.reset(self)
        self._mCodingSM.reset()
        self._mNumOfMBChar = 0

    def get_charset_name(self):
        return 'utf-8'

    def feed(self, aBuf):
        for c in aBuf:
            codingState = self._mCodingSM.next_state(c)
            if codingState == eError:
                self._mState = constants.eNotMe
                break
            elif codingState == eItsMe:
                self._mState = constants.eFoundIt
                break
            elif codingState == eStart:
                if self._mCodingSM.get_current_charlen() >= 2:
                    self._mNumOfMBChar += 1

        if self.get_state() == constants.eDetecting:
            if self.get_confidence() > constants.SHORTCUT_THRESHOLD:
                self._mState = constants.eFoundIt
        return self.get_state()

    def get_confidence(self):
        unlike = 0.99
        if self._mNumOfMBChar < 6:
            for i in xrange(0, self._mNumOfMBChar):
                unlike = unlike * ONE_CHAR_PROB

            return 1.0 - unlike
        else:
            return unlike