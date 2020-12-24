# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/big5prober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1684 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import Big5DistributionAnalysis
from .mbcssm import Big5SMModel

class Big5Prober(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(Big5SMModel)
        self._mDistributionAnalyzer = Big5DistributionAnalysis()
        self.reset()

    def get_charset_name(self):
        return 'Big5'