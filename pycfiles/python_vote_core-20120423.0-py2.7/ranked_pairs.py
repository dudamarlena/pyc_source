# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/ranked_pairs.py
# Compiled at: 2012-04-23 20:44:07
from condorcet import CondorcetSystem, CondorcetHelper
from pygraph.classes.digraph import digraph
from pygraph.algorithms.accessibility import accessibility, mutual_accessibility
from pygraph.algorithms.cycles import find_cycle
from common_functions import matching_keys
from copy import deepcopy

class RankedPairs(CondorcetSystem, CondorcetHelper):

    def __init__(self, ballots, tie_breaker=None, ballot_notation=None):
        super(RankedPairs, self).__init__(ballots, tie_breaker=tie_breaker, ballot_notation=ballot_notation)

    def condorcet_completion_method(self):
        self.rounds = []
        graph = digraph()
        graph.add_nodes(self.candidates)
        remaining_strong_pairs = deepcopy(self.strong_pairs)
        while len(remaining_strong_pairs) > 0:
            r = {}
            largest_strength = max(remaining_strong_pairs.values())
            strongest_pairs = matching_keys(remaining_strong_pairs, largest_strength)
            if len(strongest_pairs) > 1:
                r['tied_pairs'] = strongest_pairs
                strongest_pair = self.break_ties(strongest_pairs)
            else:
                strongest_pair = list(strongest_pairs)[0]
            r['pair'] = strongest_pair
            graph.add_edge(strongest_pair)
            if len(find_cycle(graph)) > 0:
                r['action'] = 'skipped'
                graph.del_edge(strongest_pair)
            else:
                r['action'] = 'added'
            del remaining_strong_pairs[strongest_pair]
            self.rounds.append(r)

        self.old_graph = self.graph
        self.graph = graph
        self.graph_winner()

    def as_dict(self):
        data = super(RankedPairs, self).as_dict()
        if hasattr(self, 'rounds'):
            data['rounds'] = self.rounds
        return data