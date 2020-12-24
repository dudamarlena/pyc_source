# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/stats/validate.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 754 bytes
"""
Module for ruleset validation.

@author: anze.vavpetic@ijs.si
"""
from .adjustment import fdr
from .significance import apply_fisher

class Validate:

    def __init__(self, kb, significance_test=apply_fisher, adjustment=fdr):
        self.kb = kb
        self.significance_test = significance_test
        self.adjustment = adjustment

    def test(self, ruleset, alpha=0.05, q=0.01):
        """
        Tests the given ruleset and returns the significant rules.
        """
        self.significance_test(ruleset)
        if self.adjustment.__name__ == 'fdr':
            ruleset = self.adjustment(ruleset, q=q)
        else:
            if self.adjustment.__name__ == 'fwer':
                ruleset = self.adjustment(ruleset, alpha=alpha)
        return ruleset