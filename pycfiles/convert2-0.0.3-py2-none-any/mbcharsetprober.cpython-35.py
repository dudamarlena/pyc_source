# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/mbcharsetprober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 3268 bytes
import sys
from . import constants
from .charsetprober import CharSetProber

class MultiByteCharSetProber(CharSetProber):

    def __init__(self):
        CharSetProber.__init__(self)
        self._mDistributionAnalyzer = None
        self._mCodingSM = None
        self._mLastChar = [0, 0]

    def reset(self):
        CharSetProber.reset(self)
        if self._mCodingSM:
            self._mCodingSM.reset()
        if self._mDistributionAnalyzer:
            self._mDistributionAnalyzer.reset()
        self._mLastChar = [
         0, 0]

    def get_charset_name(self):
        pass

    def feed(self, aBuf):
        aLen = len(aBuf)
        for i in range(0, aLen):
            codingState = self._mCodingSM.next_state(aBuf[i])
            if codingState == constants.eError:
                if constants._debug:
                    sys.stderr.write(self.get_charset_name() + ' prober hit error at byte ' + str(i) + '\n')
                self._mState = constants.eNotMe
                break
            else:
                if codingState == constants.eItsMe:
                    self._mState = constants.eFoundIt
                    break
                elif codingState == constants.eStart:
                    charLen = self._mCodingSM.get_current_charlen()
                    if i == 0:
                        self._mLastChar[1] = aBuf[0]
                        self._mDistributionAnalyzer.feed(self._mLastChar, charLen)
                    else:
                        self._mDistributionAnalyzer.feed(aBuf[i - 1:i + 1], charLen)

        self._mLastChar[0] = aBuf[(aLen - 1)]
        if self.get_state() == constants.eDetecting and self._mDistributionAnalyzer.got_enough_data() and self.get_confidence() > constants.SHORTCUT_THRESHOLD:
            self._mState = constants.eFoundIt
        return self.get_state()

    def get_confidence(self):
        return self._mDistributionAnalyzer.get_confidence()