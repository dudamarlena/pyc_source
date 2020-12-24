# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/universaldetector.py
# Compiled at: 2013-12-09 06:41:17
import constants, sys
from latin1prober import Latin1Prober
from mbcsgroupprober import MBCSGroupProber
from sbcsgroupprober import SBCSGroupProber
from escprober import EscCharSetProber
import re
MINIMUM_THRESHOLD = 0.2
ePureAscii = 0
eEscAscii = 1
eHighbyte = 2

class UniversalDetector:

    def __init__(self):
        self._highBitDetector = re.compile('[\\x80-\\xFF]')
        self._escDetector = re.compile('(\\033|~{)')
        self._mEscCharSetProber = None
        self._mCharSetProbers = []
        self.reset()
        return

    def reset(self):
        self.result = {'encoding': None, 'confidence': 0.0}
        self.done = constants.False
        self._mStart = constants.True
        self._mGotData = constants.False
        self._mInputState = ePureAscii
        self._mLastChar = ''
        if self._mEscCharSetProber:
            self._mEscCharSetProber.reset()
        for prober in self._mCharSetProbers:
            prober.reset()

        return

    def feed(self, aBuf):
        if self.done:
            return
        aLen = len(aBuf)
        if not aLen:
            return
        if not self._mGotData:
            if aBuf[:3] == '\ufeff':
                self.result = {'encoding': 'UTF-8', 'confidence': 1.0}
            elif aBuf[:4] == b'\xff\xfe\x00\x00':
                self.result = {'encoding': 'UTF-32LE', 'confidence': 1.0}
            elif aBuf[:4] == b'\x00\x00\xfe\xff':
                self.result = {'encoding': 'UTF-32BE', 'confidence': 1.0}
            elif aBuf[:4] == b'\xfe\xff\x00\x00':
                self.result = {'encoding': 'X-ISO-10646-UCS-4-3412', 'confidence': 1.0}
            elif aBuf[:4] == b'\x00\x00\xff\xfe':
                self.result = {'encoding': 'X-ISO-10646-UCS-4-2143', 'confidence': 1.0}
            elif aBuf[:2] == b'\xff\xfe':
                self.result = {'encoding': 'UTF-16LE', 'confidence': 1.0}
            elif aBuf[:2] == b'\xfe\xff':
                self.result = {'encoding': 'UTF-16BE', 'confidence': 1.0}
        self._mGotData = constants.True
        if self.result['encoding'] and self.result['confidence'] > 0.0:
            self.done = constants.True
            return
        if self._mInputState == ePureAscii:
            if self._highBitDetector.search(aBuf):
                self._mInputState = eHighbyte
            elif self._mInputState == ePureAscii and self._escDetector.search(self._mLastChar + aBuf):
                self._mInputState = eEscAscii
        self._mLastChar = aBuf[(-1)]
        if self._mInputState == eEscAscii:
            if not self._mEscCharSetProber:
                self._mEscCharSetProber = EscCharSetProber()
            if self._mEscCharSetProber.feed(aBuf) == constants.eFoundIt:
                self.result = {'encoding': self._mEscCharSetProber.get_charset_name(), 'confidence': self._mEscCharSetProber.get_confidence()}
                self.done = constants.True
        elif self._mInputState == eHighbyte:
            if not self._mCharSetProbers:
                self._mCharSetProbers = [
                 MBCSGroupProber(), SBCSGroupProber(), Latin1Prober()]
            for prober in self._mCharSetProbers:
                if prober.feed(aBuf) == constants.eFoundIt:
                    self.result = {'encoding': prober.get_charset_name(), 'confidence': prober.get_confidence()}
                    self.done = constants.True
                    break

    def close(self):
        if self.done:
            return
        else:
            if not self._mGotData:
                if constants._debug:
                    sys.stderr.write('no data received!\n')
                return
            self.done = constants.True
            if self._mInputState == ePureAscii:
                self.result = {'encoding': 'ascii', 'confidence': 1.0}
                return self.result
            if self._mInputState == eHighbyte:
                proberConfidence = None
                maxProberConfidence = 0.0
                maxProber = None
                for prober in self._mCharSetProbers:
                    if not prober:
                        continue
                    proberConfidence = prober.get_confidence()
                    if proberConfidence > maxProberConfidence:
                        maxProberConfidence = proberConfidence
                        maxProber = prober

                if maxProber and maxProberConfidence > MINIMUM_THRESHOLD:
                    self.result = {'encoding': maxProber.get_charset_name(), 'confidence': maxProber.get_confidence()}
                    return self.result
            if constants._debug:
                sys.stderr.write('no probers hit minimum threshhold\n')
                for prober in self._mCharSetProbers[0].mProbers:
                    if not prober:
                        continue
                    sys.stderr.write('%s confidence = %s\n' % (
                     prober.get_charset_name(),
                     prober.get_confidence()))

            return