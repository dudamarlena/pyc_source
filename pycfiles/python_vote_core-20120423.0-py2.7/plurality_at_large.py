# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/plurality_at_large.py
# Compiled at: 2012-04-23 20:44:07
from abstract_classes import MultipleWinnerVotingSystem
from common_functions import matching_keys
import types, copy

class PluralityAtLarge(MultipleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None, required_winners=1):
        super(PluralityAtLarge, self).__init__(ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):
        self.candidates = set()
        for ballot in self.ballots:
            if type(ballot['ballot']) != types.ListType:
                ballot['ballot'] = [
                 ballot['ballot']]
            if len(ballot['ballot']) > self.required_winners:
                raise Exception('A ballot contained too many candidates')
            self.candidates.update(set(ballot['ballot']))

        self.tallies = dict.fromkeys(self.candidates, 0)
        for ballot in self.ballots:
            for candidate in ballot['ballot']:
                self.tallies[candidate] += ballot['count']

        tallies = copy.deepcopy(self.tallies)
        winning_candidates = set()
        while len(winning_candidates) < self.required_winners:
            largest_tally = max(tallies.values())
            top_candidates = matching_keys(tallies, largest_tally)
            if len(top_candidates | winning_candidates) > self.required_winners:
                self.tied_winners = top_candidates.copy()
                while len(top_candidates | winning_candidates) > self.required_winners:
                    top_candidates.remove(self.break_ties(top_candidates, True))

            winning_candidates |= top_candidates
            for candidate in top_candidates:
                del tallies[candidate]

        self.winners = winning_candidates

    def as_dict(self):
        data = super(PluralityAtLarge, self).as_dict()
        data['tallies'] = self.tallies
        return data