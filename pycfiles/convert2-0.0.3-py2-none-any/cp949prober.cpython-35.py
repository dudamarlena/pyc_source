# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/cp949prober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1782 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import EUCKRDistributionAnalysis
from .mbcssm import CP949SMModel

class CP949Prober(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(CP949SMModel)
        self._mDistributionAnalyzer = EUCKRDistributionAnalysis()
        self.reset()

    def get_charset_name(self):
        return 'CP949'