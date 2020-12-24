# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/schulze_by_graph.py
# Compiled at: 2012-04-23 20:44:13
from schulze_method import SchulzeMethod
from schulze_helper import SchulzeHelper
from abstract_classes import AbstractOrderingVotingSystem
from pygraph.classes.digraph import digraph

class SchulzeMethodByGraph(SchulzeMethod):

    def __init__(self, edges, tie_breaker=None, ballot_notation=None):
        self.edges = edges
        super(SchulzeMethodByGraph, self).__init__([], tie_breaker=tie_breaker, ballot_notation=ballot_notation)

    def standardize_ballots(self, ballots, ballot_notation):
        self.ballots = []
        self.candidates = set([ edge[0] for edge, weight in self.edges.iteritems() ]) | set([ edge[1] for edge, weight in self.edges.iteritems() ])

    def ballots_into_graph(self, candidates, ballots):
        graph = digraph()
        graph.add_nodes(candidates)
        for edge in self.edges.iteritems():
            graph.add_edge(edge[0], edge[1])

        return graph


class SchulzeNPRByGraph(AbstractOrderingVotingSystem, SchulzeHelper):

    def __init__(self, edges, winner_threshold=None, tie_breaker=None, ballot_notation=None):
        self.edges = edges
        self.candidates = set([ edge[0] for edge, weight in edges.iteritems() ]) | set([ edge[1] for edge, weight in edges.iteritems() ])
        super(SchulzeNPRByGraph, self).__init__([], single_winner_class=SchulzeMethodByGraph, winner_threshold=winner_threshold, tie_breaker=tie_breaker)

    def ballots_without_candidate(self, ballots, candidate):
        self.edges = dict([ (edge, weight) for edge, weight in self.edges.iteritems() if edge[0] != candidate and edge[1] != candidate ])
        return self.edges

    def calculate_results(self):
        self.ballots = self.edges
        super(SchulzeNPRByGraph, self).calculate_results()