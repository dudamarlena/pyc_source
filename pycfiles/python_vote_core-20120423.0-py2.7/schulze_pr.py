# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/schulze_pr.py
# Compiled at: 2012-04-23 20:44:11
from schulze_helper import SchulzeHelper
from abstract_classes import OrderingVotingSystem
from pygraph.classes.digraph import digraph

class SchulzePR(OrderingVotingSystem, SchulzeHelper):

    def __init__(self, ballots, tie_breaker=None, winner_threshold=None, ballot_notation=None):
        self.standardize_ballots(ballots, ballot_notation)
        super(SchulzePR, self).__init__(self.ballots, tie_breaker=tie_breaker, winner_threshold=winner_threshold)

    def calculate_results(self):
        remaining_candidates = self.candidates.copy()
        self.order = []
        self.rounds = []
        if self.winner_threshold == None:
            winner_threshold = len(self.candidates)
        else:
            winner_threshold = min(len(self.candidates), self.winner_threshold + 1)
        for self.required_winners in range(1, winner_threshold):
            self.generate_completed_patterns()
            self.generate_vote_management_graph()
            self.graph = digraph()
            self.graph.add_nodes(remaining_candidates)
            self.winners = set([])
            self.tied_winners = set([])
            for candidate_from in remaining_candidates:
                other_candidates = sorted(list(remaining_candidates - set([candidate_from])))
                for candidate_to in other_candidates:
                    completed = self.proportional_completion(candidate_from, set([candidate_to]) | set(self.order))
                    weight = self.strength_of_vote_management(completed)
                    if weight > 0:
                        self.graph.add_edge((candidate_to, candidate_from), weight)

            self.schwartz_set_heuristic()
            self.order.append(self.winner)
            round = {'winner': self.winner}
            if len(self.tied_winners) > 0:
                round['tied_winners'] = self.tied_winners
            self.rounds.append(round)
            remaining_candidates -= set([self.winner])
            del self.winner
            del self.actions
            if hasattr(self, 'tied_winners'):
                del self.tied_winners

        if self.winner_threshold == None or self.winner_threshold == len(self.candidates):
            self.rounds.append({'winner': list(remaining_candidates)[0]})
            self.order.append(list(remaining_candidates)[0])
        del self.winner_threshold
        return

    def as_dict(self):
        data = super(SchulzePR, self).as_dict()
        data['rounds'] = self.rounds
        return data