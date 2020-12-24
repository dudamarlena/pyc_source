# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/chardet/gb2312prober.py
# Compiled at: 2018-01-22 17:51:30
# Size of source mod 2**32: 1681 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import GB2312DistributionAnalysis
from .mbcssm import GB2312SMModel

class GB2312Prober(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(GB2312SMModel)
        self._mDistributionAnalyzer = GB2312DistributionAnalysis()
        self.reset()

    def get_charset_name(self):
        return 'GB2312'