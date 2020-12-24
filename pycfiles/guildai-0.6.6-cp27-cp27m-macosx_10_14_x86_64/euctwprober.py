# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/chardet/euctwprober.py
# Compiled at: 2019-09-10 15:18:29
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import EUCTWDistributionAnalysis
from .mbcssm import EUCTW_SM_MODEL

class EUCTWProber(MultiByteCharSetProber):

    def __init__(self):
        super(EUCTWProber, self).__init__()
        self.coding_sm = CodingStateMachine(EUCTW_SM_MODEL)
        self.distribution_analyzer = EUCTWDistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'EUC-TW'

    @property
    def language(self):
        return 'Taiwan'