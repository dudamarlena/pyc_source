# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/stats/adjustment.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 936 bytes
__doc__ = '\nMultiple-testing adjustment methods.\n\n@author: anze.vavpetic@ijs.si\n'

def _holdout(ruleset):
    """
    TODO: The holdout approach.
    """
    return ruleset


def fwer(ruleset, alpha=0.05):
    """
    The Holm-Bonferroni direct adjustment method to control the FWER.
    """
    m = float(len(list(ruleset)))
    ruleset = sorted(ruleset, key=(lambda r: r.pval))
    for k, rule in enumerate(ruleset):
        if rule.pval > alpha / (m + 1 - (k + 1)):
            ruleset = ruleset[:k]
            break

    return ruleset


def fdr(ruleset, q=0.05):
    """
    The Benjamini-Hochberg-Yekutieli direct adjustment
    method to control the FDR.
    """
    m = float(len(list(ruleset)))
    ruleset = sorted(ruleset, key=(lambda r: r.pval))
    for k, rule in enumerate(ruleset):
        if rule.pval > (k + 1) * q / m:
            ruleset = ruleset[:k]
            break

    return ruleset


def none(ruleset):
    return ruleset