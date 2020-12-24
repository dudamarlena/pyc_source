# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/chardistribution.py
# Compiled at: 2013-12-09 06:41:17
import constants
from euctwfreq import EUCTWCharToFreqOrder, EUCTW_TABLE_SIZE, EUCTW_TYPICAL_DISTRIBUTION_RATIO
from euckrfreq import EUCKRCharToFreqOrder, EUCKR_TABLE_SIZE, EUCKR_TYPICAL_DISTRIBUTION_RATIO
from gb2312freq import GB2312CharToFreqOrder, GB2312_TABLE_SIZE, GB2312_TYPICAL_DISTRIBUTION_RATIO
from big5freq import Big5CharToFreqOrder, BIG5_TABLE_SIZE, BIG5_TYPICAL_DISTRIBUTION_RATIO
from jisfreq import JISCharToFreqOrder, JIS_TABLE_SIZE, JIS_TYPICAL_DISTRIBUTION_RATIO
ENOUGH_DATA_THRESHOLD = 1024
SURE_YES = 0.99
SURE_NO = 0.01

class CharDistributionAnalysis:

    def __init__(self):
        self._mCharToFreqOrder = None
        self._mTableSize = None
        self._mTypicalDistributionRatio = None
        self.reset()
        return

    def reset(self):
        """reset analyser, clear any state"""
        self._mDone = constants.False
        self._mTotalChars = 0
        self._mFreqChars = 0

    def feed(self, aStr, aCharLen):
        """feed a character with known length"""
        if aCharLen == 2:
            order = self.get_order(aStr)
        else:
            order = -1
        if order >= 0:
            self._mTotalChars += 1
            if order < self._mTableSize:
                if 512 > self._mCharToFreqOrder[order]:
                    self._mFreqChars += 1

    def get_confidence(self):
        """return confidence based on existing data"""
        if self._mTotalChars <= 0:
            return SURE_NO
        if self._mTotalChars != self._mFreqChars:
            r = self._mFreqChars / ((self._mTotalChars - self._mFreqChars) * self._mTypicalDistributionRatio)
            if r < SURE_YES:
                return r
        return SURE_YES

    def got_enough_data(self):
        return self._mTotalChars > ENOUGH_DATA_THRESHOLD

    def get_order(self, aStr):
        return -1


class EUCTWDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        CharDistributionAnalysis.__init__(self)
        self._mCharToFreqOrder = EUCTWCharToFreqOrder
        self._mTableSize = EUCTW_TABLE_SIZE
        self._mTypicalDistributionRatio = EUCTW_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, aStr):
        if aStr[0] >= b'\xc4':
            return 94 * (ord(aStr[0]) - 196) + ord(aStr[1]) - 161
        else:
            return -1


class EUCKRDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        CharDistributionAnalysis.__init__(self)
        self._mCharToFreqOrder = EUCKRCharToFreqOrder
        self._mTableSize = EUCKR_TABLE_SIZE
        self._mTypicalDistributionRatio = EUCKR_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, aStr):
        if aStr[0] >= b'\xb0':
            return 94 * (ord(aStr[0]) - 176) + ord(aStr[1]) - 161
        else:
            return -1


class GB2312DistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        CharDistributionAnalysis.__init__(self)
        self._mCharToFreqOrder = GB2312CharToFreqOrder
        self._mTableSize = GB2312_TABLE_SIZE
        self._mTypicalDistributionRatio = GB2312_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, aStr):
        if aStr[0] >= b'\xb0' and aStr[1] >= b'\xa1':
            return 94 * (ord(aStr[0]) - 176) + ord(aStr[1]) - 161
        else:
            return -1


class Big5DistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        CharDistributionAnalysis.__init__(self)
        self._mCharToFreqOrder = Big5CharToFreqOrder
        self._mTableSize = BIG5_TABLE_SIZE
        self._mTypicalDistributionRatio = BIG5_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, aStr):
        if aStr[0] >= b'\xa4':
            if aStr[1] >= b'\xa1':
                return 157 * (ord(aStr[0]) - 164) + ord(aStr[1]) - 161 + 63
            else:
                return 157 * (ord(aStr[0]) - 164) + ord(aStr[1]) - 64

        else:
            return -1


class SJISDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        CharDistributionAnalysis.__init__(self)
        self._mCharToFreqOrder = JISCharToFreqOrder
        self._mTableSize = JIS_TABLE_SIZE
        self._mTypicalDistributionRatio = JIS_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, aStr):
        if aStr[0] >= b'\x81' and aStr[0] <= b'\x9f':
            order = 188 * (ord(aStr[0]) - 129)
        elif aStr[0] >= b'\xe0' and aStr[0] <= b'\xef':
            order = 188 * (ord(aStr[0]) - 224 + 31)
        else:
            return -1
        order = order + ord(aStr[1]) - 64
        if aStr[1] > '\x7f':
            order = -1
        return order


class EUCJPDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        CharDistributionAnalysis.__init__(self)
        self._mCharToFreqOrder = JISCharToFreqOrder
        self._mTableSize = JIS_TABLE_SIZE
        self._mTypicalDistributionRatio = JIS_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, aStr):
        if aStr[0] >= b'\xa0':
            return 94 * (ord(aStr[0]) - 161) + ord(aStr[1]) - 161
        else:
            return -1