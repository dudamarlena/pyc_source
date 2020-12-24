# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/condorcet.py
# Compiled at: 2012-04-23 20:44:15
from abc import ABCMeta, abstractmethod
from abstract_classes import SingleWinnerVotingSystem
from pygraph.classes.digraph import digraph
import itertools

class CondorcetHelper(object):

    def standardize_ballots(self, ballots, ballot_notation):
        self.ballots = ballots
        if ballot_notation == 'grouping':
            for ballot in self.ballots:
                ballot['ballot'].reverse()
                new_ballot = {}
                r = 0
                for rank in ballot['ballot']:
                    r += 1
                    for candidate in rank:
                        new_ballot[candidate] = r

                ballot['ballot'] = new_ballot

        else:
            if ballot_notation == 'ranking':
                for ballot in self.ballots:
                    for candidate, rating in ballot['ballot'].iteritems():
                        ballot['ballot'][candidate] = -float(rating)

            else:
                if ballot_notation == 'rating' or ballot_notation == None:
                    for ballot in self.ballots:
                        for candidate, rating in ballot['ballot'].iteritems():
                            ballot['ballot'][candidate] = float(rating)

                else:
                    print ballot_notation
                    raise Exception('Unknown notation specified')
                self.candidates = set()
                for ballot in self.ballots:
                    self.candidates |= set(ballot['ballot'].keys())

            for ballot in self.ballots:
                lowest_preference = min(ballot['ballot'].values()) - 1
                for candidate in self.candidates - set(ballot['ballot'].keys()):
                    ballot['ballot'][candidate] = lowest_preference

        return

    def graph_winner(self):
        losing_candidates = set([ edge[1] for edge in self.graph.edges() ])
        winning_candidates = set(self.graph.nodes()) - losing_candidates
        if len(winning_candidates) == 1:
            self.winner = list(winning_candidates)[0]
        elif len(winning_candidates) > 1:
            self.tied_winners = winning_candidates
            self.winner = self.break_ties(winning_candidates)
        else:
            self.condorcet_completion_method()

    @staticmethod
    def ballots_into_graph(candidates, ballots):
        graph = digraph()
        graph.add_nodes(candidates)
        for pair in itertools.permutations(candidates, 2):
            graph.add_edge(pair, sum([ ballot['count'] for ballot in ballots if ballot['ballot'][pair[0]] > ballot['ballot'][pair[1]]
                                     ]))

        return graph

    @staticmethod
    def edge_weights(graph):
        return dict([ (edge, graph.edge_weight(edge)) for edge in graph.edges()
                    ])

    @staticmethod
    def remove_weak_edges(graph):
        for pair in itertools.combinations(graph.nodes(), 2):
            pairs = (
             pair, (pair[1], pair[0]))
            weights = (graph.edge_weight(pairs[0]), graph.edge_weight(pairs[1]))
            if weights[0] >= weights[1]:
                graph.del_edge(pairs[1])
            if weights[1] >= weights[0]:
                graph.del_edge(pairs[0])


class CondorcetSystem(SingleWinnerVotingSystem, CondorcetHelper):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, tie_breaker=None, ballot_notation=None):
        self.standardize_ballots(ballots, ballot_notation)
        super(CondorcetSystem, self).__init__(self.ballots, tie_breaker=tie_breaker)

    def calculate_results(self):
        self.graph = self.ballots_into_graph(self.candidates, self.ballots)
        self.pairs = self.edge_weights(self.graph)
        self.remove_weak_edges(self.graph)
        self.strong_pairs = self.edge_weights(self.graph)
        self.graph_winner()

    def as_dict(self):
        data = super(CondorcetSystem, self).as_dict()
        if hasattr(self, 'pairs'):
            data['pairs'] = self.pairs
        if hasattr(self, 'strong_pairs'):
            data['strong_pairs'] = self.strong_pairs
        if hasattr(self, 'tied_winners'):
            data['tied_winners'] = self.tied_winners
        return data