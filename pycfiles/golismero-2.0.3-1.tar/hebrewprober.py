# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/hebrewprober.py
# Compiled at: 2013-12-09 06:41:17
from charsetprober import CharSetProber
import constants
FINAL_KAF = b'\xea'
NORMAL_KAF = b'\xeb'
FINAL_MEM = b'\xed'
NORMAL_MEM = b'\xee'
FINAL_NUN = b'\xef'
NORMAL_NUN = b'\xf0'
FINAL_PE = b'\xf3'
NORMAL_PE = b'\xf4'
FINAL_TSADI = b'\xf5'
NORMAL_TSADI = b'\xf6'
MIN_FINAL_CHAR_DISTANCE = 5
MIN_MODEL_DISTANCE = 0.01
VISUAL_HEBREW_NAME = 'ISO-8859-8'
LOGICAL_HEBREW_NAME = 'windows-1255'

class HebrewProber(CharSetProber):

    def __init__(self):
        CharSetProber.__init__(self)
        self._mLogicalProber = None
        self._mVisualProber = None
        self.reset()
        return

    def reset(self):
        self._mFinalCharLogicalScore = 0
        self._mFinalCharVisualScore = 0
        self._mPrev = ' '
        self._mBeforePrev = ' '

    def set_model_probers(self, logicalProber, visualProber):
        self._mLogicalProber = logicalProber
        self._mVisualProber = visualProber

    def is_final(self, c):
        return c in [FINAL_KAF, FINAL_MEM, FINAL_NUN, FINAL_PE, FINAL_TSADI]

    def is_non_final(self, c):
        return c in [NORMAL_KAF, NORMAL_MEM, NORMAL_NUN, NORMAL_PE]

    def feed(self, aBuf):
        if self.get_state() == constants.eNotMe:
            return constants.eNotMe
        aBuf = self.filter_high_bit_only(aBuf)
        for cur in aBuf:
            if cur == ' ':
                if self._mBeforePrev != ' ':
                    if self.is_final(self._mPrev):
                        self._mFinalCharLogicalScore += 1
                    elif self.is_non_final(self._mPrev):
                        self._mFinalCharVisualScore += 1
            elif self._mBeforePrev == ' ' and self.is_final(self._mPrev) and cur != ' ':
                self._mFinalCharVisualScore += 1
            self._mBeforePrev = self._mPrev
            self._mPrev = cur

        return constants.eDetecting

    def get_charset_name(self):
        finalsub = self._mFinalCharLogicalScore - self._mFinalCharVisualScore
        if finalsub >= MIN_FINAL_CHAR_DISTANCE:
            return LOGICAL_HEBREW_NAME
        if finalsub <= -MIN_FINAL_CHAR_DISTANCE:
            return VISUAL_HEBREW_NAME
        modelsub = self._mLogicalProber.get_confidence() - self._mVisualProber.get_confidence()
        if modelsub > MIN_MODEL_DISTANCE:
            return LOGICAL_HEBREW_NAME
        if modelsub < -MIN_MODEL_DISTANCE:
            return VISUAL_HEBREW_NAME
        if finalsub < 0.0:
            return VISUAL_HEBREW_NAME
        return LOGICAL_HEBREW_NAME

    def get_state(self):
        if self._mLogicalProber.get_state() == constants.eNotMe and self._mVisualProber.get_state() == constants.eNotMe:
            return constants.eNotMe
        return constants.eDetecting