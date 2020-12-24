# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/stats/significance.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1177 bytes
__doc__ = '\nSignificance testing methods.\n\n@author: anze.vavpetic@ijs.si\n'
import scipy.stats as st

def is_redundant(rule, new_rule):
    """
    Computes the redundancy coefficient of a new rule compared to its
    immediate generalization.

    Rules with a coeff > 1 are deemed non-redundant.
    """
    return _fisher(new_rule, 'greater') > _fisher(rule, 'greater')


def fisher(rule):
    """
    Fisher's p-value for one rule.
    """
    return _fisher(rule, 'two-sided')


def _fisher(rule, alternative):
    """
    Fisher's p-value for one rule.
        fisher.two_tail   ==> alternative = 'two-sided'
        fisher.left_tail  ==> alternative = 'less'
        fisher.right_tail ==> alternative = 'greater'
    """
    N = float(len(rule.kb.examples))
    nX = float(rule.coverage)
    nY = rule.kb.distribution[rule.target]
    nXY = rule.distribution[rule.target]
    nXnotY = nX - nXY
    nnotXY = nY - nXY
    nnotXnotY = N - nXnotY - nnotXY
    return st.fisher_exact([[nXY, nXnotY], [nnotXY, nnotXnotY]], alternative=alternative)[1]


def apply_fisher(ruleset):
    """
    Fisher's exact test to test rule significance.
    """
    for rule in ruleset:
        rule.pval = fisher(rule)