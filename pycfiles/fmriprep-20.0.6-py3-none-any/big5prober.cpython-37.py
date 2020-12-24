# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/chardet/big5prober.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 1757 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import Big5DistributionAnalysis
from .mbcssm import BIG5_SM_MODEL

class Big5Prober(MultiByteCharSetProber):

    def __init__(self):
        super(Big5Prober, self).__init__()
        self.coding_sm = CodingStateMachine(BIG5_SM_MODEL)
        self.distribution_analyzer = Big5DistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'Big5'

    @property
    def language(self):
        return 'Chinese'