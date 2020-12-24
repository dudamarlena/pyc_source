# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/stats/validate.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 754 bytes
__doc__ = '\nModule for ruleset validation.\n\n@author: anze.vavpetic@ijs.si\n'
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
        elif self.adjustment.__name__ == 'fwer':
            ruleset = self.adjustment(ruleset, alpha=alpha)
        return ruleset