# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/chardet/euckrprober.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 1748 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import EUCKRDistributionAnalysis
from .mbcssm import EUCKR_SM_MODEL

class EUCKRProber(MultiByteCharSetProber):

    def __init__(self):
        super(EUCKRProber, self).__init__()
        self.coding_sm = CodingStateMachine(EUCKR_SM_MODEL)
        self.distribution_analyzer = EUCKRDistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'EUC-KR'

    @property
    def language(self):
        return 'Korean'