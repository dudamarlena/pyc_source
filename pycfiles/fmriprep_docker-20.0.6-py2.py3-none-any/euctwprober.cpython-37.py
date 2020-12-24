# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_vendor/chardet/euctwprober.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 1747 bytes
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