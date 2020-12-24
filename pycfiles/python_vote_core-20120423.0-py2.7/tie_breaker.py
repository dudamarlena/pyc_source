# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/tie_breaker.py
# Compiled at: 2012-04-23 20:44:05
import random, types
from copy import copy

class TieBreaker(object):

    def __init__(self, candidate_range):
        self.ties_broken = False
        self.random_ordering = list(candidate_range)
        if type(candidate_range) != types.ListType:
            random.shuffle(self.random_ordering)

    def break_ties(self, tied_candidates, reverse=False):
        self.ties_broken = True
        random_ordering = copy(self.random_ordering)
        if reverse:
            random_ordering.reverse()
        if getattr(list(tied_candidates)[0], '__iter__', False):
            result = self.break_complex_ties(tied_candidates, random_ordering)
        else:
            result = self.break_simple_ties(tied_candidates, random_ordering)
        return result

    @staticmethod
    def break_simple_ties(tied_candidates, random_ordering):
        for candidate in random_ordering:
            if candidate in tied_candidates:
                return candidate

    @staticmethod
    def break_complex_ties(tied_candidates, random_ordering):
        max_columns = len(list(tied_candidates)[0])
        column = 0
        while len(tied_candidates) > 1 and column < max_columns:
            min_index = min(random_ordering.index(list(candidate)[column]) for candidate in tied_candidates)
            tied_candidates = set([ candidate for candidate in tied_candidates if candidate[column] == random_ordering[min_index] ])
            column += 1

        return list(tied_candidates)[0]

    def as_list(self):
        return self.random_ordering

    def __str__(self):
        return '[%s]' % ('>').join(self.random_ordering)