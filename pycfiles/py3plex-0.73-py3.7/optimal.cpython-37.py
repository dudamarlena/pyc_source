# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/learners/optimal.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1859 bytes
"""
Main learner class.

@author: anze.vavpetic@ijs.si
"""
from collections import defaultdict
from itertools import combinations
from ..core import UnaryPredicate, Rule, Example
from core.settings import logger
from stats.significance import is_redundant
from stats.scorefunctions import interesting
from .learner import Learner

class OptimalLearner(Learner):
    __doc__ = '\n    Finds the optimal top-k rules.\n    '

    def __init__(self, kb, n=None, min_sup=1, sim=1, depth=4, target=None, use_negations=False, optimal_subclass=True):
        Learner.__init__(self, kb, n=n, min_sup=min_sup, sim=sim, depth=depth, target=target,
          use_negations=use_negations)

    def induce(self):
        """
        Induces rules for the given knowledge base.
        """
        kb = self.kb
        has_min_sup = lambda pred: kb.get_members(pred).count() >= self.min_sup
        all_predicates = filter(has_min_sup, kb.predicates)
        rules = []
        for depth in range(1, self.depth + 1):
            for attrs in combinations(all_predicates, depth):
                rule = Rule(kb, predicates=(self._labels_to_predicates(attrs)), target=(self.target))
                rules.append(rule)

        rules = sorted(rules, key=(lambda r: r.score), reverse=True)
        return rules[:self.n]

    def _labels_to_predicates(self, labels):
        predicates = []
        producer_pred = None
        for label in labels:
            members = self.kb.get_members(label)
            predicates.append(UnaryPredicate(label, members, (self.kb), producer_pred=producer_pred,
              custom_var_name='X'))
            producer_pred = predicates[(-1)]

        return predicates