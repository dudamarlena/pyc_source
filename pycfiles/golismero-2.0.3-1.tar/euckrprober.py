# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/chardet/euckrprober.py
# Compiled at: 2013-12-09 06:41:17
from mbcharsetprober import MultiByteCharSetProber
from codingstatemachine import CodingStateMachine
from chardistribution import EUCKRDistributionAnalysis
from mbcssm import EUCKRSMModel

class EUCKRProber(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(EUCKRSMModel)
        self._mDistributionAnalyzer = EUCKRDistributionAnalysis()
        self.reset()

    def get_charset_name(self):
        return 'EUC-KR'