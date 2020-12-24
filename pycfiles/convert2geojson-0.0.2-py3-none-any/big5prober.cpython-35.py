# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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