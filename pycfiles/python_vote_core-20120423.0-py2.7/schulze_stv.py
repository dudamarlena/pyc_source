# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/schulze_stv.py
# Compiled at: 2012-04-23 22:56:55
from abstract_classes import MultipleWinnerVotingSystem
from schulze_helper import SchulzeHelper
from pygraph.classes.digraph import digraph
import itertools

class SchulzeSTV(MultipleWinnerVotingSystem, SchulzeHelper):

    def __init__(self, ballots, tie_breaker=None, required_winners=1, ballot_notation=None):
        self.standardize_ballots(ballots, ballot_notation)
        super(SchulzeSTV, self).__init__(self.ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):
        super(SchulzeSTV, self).calculate_results()
        if hasattr(self, 'winners'):
            return
        self.generate_completed_patterns()
        self.generate_vote_management_graph()
        self.graph = digraph()
        for candidate_set in itertools.combinations(self.candidates, self.required_winners):
            self.graph.add_nodes([tuple(sorted(list(candidate_set)))])

        for candidate_set in itertools.combinations(self.candidates, self.required_winners + 1):
            for candidate in candidate_set:
                other_candidates = sorted(set(candidate_set) - set([candidate]))
                completed = self.proportional_completion(candidate, other_candidates)
                weight = self.strength_of_vote_management(completed)
                if weight > 0:
                    for subset in itertools.combinations(other_candidates, len(other_candidates) - 1):
                        self.graph.add_edge((tuple(other_candidates), tuple(sorted(list(subset) + [candidate]))), weight)

        self.graph_winner()
        self.winners = set(self.winner)
        del self.winner

    def as_dict(self):
        data = super(SchulzeSTV, self).as_dict()
        if hasattr(self, 'actions'):
            data['actions'] = self.actions
        return data