# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/chardet/euckrprober.py
# Compiled at: 2020-04-16 14:32:20
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