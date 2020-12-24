# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_vendor/chardet/cp949prober.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 1855 bytes
from .chardistribution import EUCKRDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import CP949_SM_MODEL

class CP949Prober(MultiByteCharSetProber):

    def __init__(self):
        super(CP949Prober, self).__init__()
        self.coding_sm = CodingStateMachine(CP949_SM_MODEL)
        self.distribution_analyzer = EUCKRDistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'CP949'

    @property
    def language(self):
        return 'Korean'