# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/hebrewprober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 13359 bytes
from .charsetprober import CharSetProber
from .constants import eNotMe, eDetecting
from .compat import wrap_ord
FINAL_KAF = 234
NORMAL_KAF = 235
FINAL_MEM = 237
NORMAL_MEM = 238
FINAL_NUN = 239
NORMAL_NUN = 240
FINAL_PE = 243
NORMAL_PE = 244
FINAL_TSADI = 245
NORMAL_TSADI = 246
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

    def reset(self):
        self._mFinalCharLogicalScore = 0
        self._mFinalCharVisualScore = 0
        self._mPrev = ' '
        self._mBeforePrev = ' '

    def set_model_probers(self, logicalProber, visualProber):
        self._mLogicalProber = logicalProber
        self._mVisualProber = visualProber

    def is_final(self, c):
        return wrap_ord(c) in [FINAL_KAF, FINAL_MEM, FINAL_NUN, FINAL_PE,
         FINAL_TSADI]

    def is_non_final(self, c):
        return wrap_ord(c) in [NORMAL_KAF, NORMAL_MEM, NORMAL_NUN, NORMAL_PE]

    def feed(self, aBuf):
        if self.get_state() == eNotMe:
            return eNotMe
        else:
            aBuf = self.filter_high_bit_only(aBuf)
            for cur in aBuf:
                if cur == ' ':
                    if self._mBeforePrev != ' ':
                        if self.is_final(self._mPrev):
                            self._mFinalCharLogicalScore += 1
                        elif self.is_non_final(self._mPrev):
                            self._mFinalCharVisualScore += 1
                else:
                    if self._mBeforePrev == ' ':
                        if self.is_final(self._mPrev):
                            if cur != ' ':
                                self._mFinalCharVisualScore += 1
                self._mBeforePrev = self._mPrev
                self._mPrev = cur

            return eDetecting

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
        else:
            if finalsub < 0.0:
                return VISUAL_HEBREW_NAME
            return LOGICAL_HEBREW_NAME

    def get_state(self):
        if self._mLogicalProber.get_state() == eNotMe:
            if self._mVisualProber.get_state() == eNotMe:
                return eNotMe
        return eDetecting