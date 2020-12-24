# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/chardet/chardet/cp949prober.py
# Compiled at: 2019-11-10 08:27:46
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