# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/packages/requests/packages/chardet/euctwprober.py
# Compiled at: 2016-06-30 06:13:10
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