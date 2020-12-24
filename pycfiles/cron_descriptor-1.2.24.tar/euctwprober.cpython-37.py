# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/chardet/chardet/euctwprober.py
# Compiled at: 2019-11-10 08:27:46
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