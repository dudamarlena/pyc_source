# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/chardet/gb2312prober.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 1754 bytes
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import GB2312DistributionAnalysis
from .mbcssm import GB2312_SM_MODEL

class GB2312Prober(MultiByteCharSetProber):

    def __init__(self):
        super(GB2312Prober, self).__init__()
        self.coding_sm = CodingStateMachine(GB2312_SM_MODEL)
        self.distribution_analyzer = GB2312DistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'GB2312'

    @property
    def language(self):
        return 'Chinese'