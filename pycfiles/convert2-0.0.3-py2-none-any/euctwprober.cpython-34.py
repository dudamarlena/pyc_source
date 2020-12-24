# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/euctwprober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1676 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import EUCTWDistributionAnalysis
from .mbcssm import EUCTWSMModel

class EUCTWProber(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(EUCTWSMModel)
        self._mDistributionAnalyzer = EUCTWDistributionAnalysis()
        self.reset()

    def get_charset_name(self):
        return 'EUC-TW'