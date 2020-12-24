# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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