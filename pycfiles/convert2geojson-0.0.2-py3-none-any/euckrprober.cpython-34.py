# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/euckrprober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1675 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import EUCKRDistributionAnalysis
from .mbcssm import EUCKRSMModel

class EUCKRProber(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(EUCKRSMModel)
        self._mDistributionAnalyzer = EUCKRDistributionAnalysis()
        self.reset()

    def get_charset_name(self):
        return 'EUC-KR'