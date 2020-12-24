# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_vendor/chardet/gb2312prober.py
# Compiled at: 2020-01-10 16:25:21
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