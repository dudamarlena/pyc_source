# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/schulze_helper.py
# Compiled at: 2012-04-23 22:57:33
from pygraph.algorithms.accessibility import accessibility, mutual_accessibility
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import maximum_flow
from condorcet import CondorcetHelper
from common_functions import matching_keys, unique_permutations
PREFERRED_LESS = 1
PREFERRED_SAME = 2
PREFERRED_MORE = 3
STRENGTH_TOLERANCE = 1e-10
STRENGTH_THRESHOLD = 0.1

class SchulzeHelper(CondorcetHelper):

    def condorcet_completion_method(self):
        self.schwartz_set_heuristic()

    def schwartz_set_heuristic(self):
        self.actions = []
        while len(self.graph.edges()) > 0:
            access = accessibility(self.graph)
            mutual_access = mutual_accessibility(self.graph)
            candidates_to_remove = set()
            for candidate in self.graph.nodes():
                candidates_to_remove |= set(access[candidate]) - set(mutual_access[candidate])

            if len(candidates_to_remove) > 0:
                self.actions.append({'nodes': candidates_to_remove})
                for candidate in candidates_to_remove:
                    self.graph.del_node(candidate)

            else:
                edge_weights = self.edge_weights(self.graph)
                self.actions.append({'edges': matching_keys(edge_weights, min(edge_weights.values()))})
                for edge in self.actions[(-1)]['edges']:
                    self.graph.del_edge(edge)

        self.graph_winner()

    def generate_vote_management_graph(self):
        self.vote_management_graph = digraph()
        self.vote_management_graph.add_nodes(self.completed_patterns)
        self.vote_management_graph.del_node(tuple([PREFERRED_MORE] * self.required_winners))
        self.pattern_nodes = self.vote_management_graph.nodes()
        self.vote_management_graph.add_nodes(['source', 'sink'])
        for pattern_node in self.pattern_nodes:
            self.vote_management_graph.add_edge(('source', pattern_node))

        for i in range(self.required_winners):
            self.vote_management_graph.add_node(i)

        for pattern_node in self.pattern_nodes:
            for i in range(self.required_winners):
                if pattern_node[i] == 1:
                    self.vote_management_graph.add_edge((pattern_node, i))

        for i in range(self.required_winners):
            self.vote_management_graph.add_edge((i, 'sink'))

    def generate_completed_patterns(self):
        self.completed_patterns = []
        for i in range(0, self.required_winners + 1):
            for pattern in unique_permutations([
             PREFERRED_LESS] * (self.required_winners - i) + [
             PREFERRED_MORE] * i):
                self.completed_patterns.append(tuple(pattern))

    def proportional_completion(self, candidate, other_candidates):
        profile = dict(zip(self.completed_patterns, [0] * len(self.completed_patterns)))
        for ballot in self.ballots:
            pattern = []
            for other_candidate in other_candidates:
                if ballot['ballot'][candidate] < ballot['ballot'][other_candidate]:
                    pattern.append(PREFERRED_LESS)
                elif ballot['ballot'][candidate] == ballot['ballot'][other_candidate]:
                    pattern.append(PREFERRED_SAME)
                else:
                    pattern.append(PREFERRED_MORE)

            pattern = tuple(pattern)
            if pattern not in profile:
                profile[pattern] = 0.0
            profile[pattern] += ballot['count']

        weight_sum = sum(profile.values())
        for pattern in sorted(profile.keys(), key=lambda pattern: pattern.count(PREFERRED_SAME), reverse=True):
            if pattern.count(PREFERRED_SAME) == 0:
                break
            self.proportional_completion_round(pattern, profile)

        try:
            assert round(weight_sum, 5) == round(sum(profile.values()), 5)
        except:
            print 'Proportional completion broke (went from %s to %s)' % (weight_sum, sum(profile.values()))

        return profile

    def proportional_completion_round(self, completion_pattern, profile):
        weight_sum = sum(profile.values())
        completion_pattern_weight = profile[completion_pattern]
        del profile[completion_pattern]
        patterns_to_consider = {}
        for pattern in profile.keys():
            append = False
            append_target = []
            for i in range(len(completion_pattern)):
                if completion_pattern[i] == PREFERRED_SAME:
                    append_target.append(pattern[i])
                    if pattern[i] != PREFERRED_SAME:
                        append = True
                else:
                    append_target.append(completion_pattern[i])

            append_target = tuple(append_target)
            if append == True and append_target in profile:
                append_target = tuple(append_target)
                if append_target not in patterns_to_consider:
                    patterns_to_consider[append_target] = set()
                patterns_to_consider[append_target].add(pattern)

        denominator = 0
        for append_target, patterns in patterns_to_consider.items():
            for pattern in patterns:
                denominator += profile[pattern]

        for pattern in patterns_to_consider.keys():
            if denominator == 0:
                profile[pattern] += completion_pattern_weight / len(patterns_to_consider)
            else:
                if pattern not in profile:
                    profile[pattern] = 0
                profile[pattern] += sum(profile[considered_pattern] for considered_pattern in patterns_to_consider[pattern]) * completion_pattern_weight / denominator

        try:
            assert round(weight_sum, 5) == round(sum(profile.values()), 5)
        except:
            print 'Proportional completion round broke (went from %s to %s)' % (weight_sum, sum(profile.values()))

        return profile

    def strength_of_vote_management(self, voter_profile):
        for pattern in self.pattern_nodes:
            self.vote_management_graph.set_edge_weight(('source', pattern), voter_profile[pattern])
            for i in range(self.required_winners):
                if pattern[i] == 1:
                    self.vote_management_graph.set_edge_weight((pattern, i), voter_profile[pattern])

        r = [
         (float(sum(voter_profile.values())) - voter_profile[tuple([PREFERRED_MORE] * self.required_winners)]) / self.required_winners]
        while len(r) < 2 or r[(-2)] - r[(-1)] > STRENGTH_TOLERANCE:
            for i in range(self.required_winners):
                self.vote_management_graph.set_edge_weight((i, 'sink'), r[(-1)])

            max_flow = maximum_flow(self.vote_management_graph, 'source', 'sink')
            sink_sum = sum(v for k, v in max_flow[0].iteritems() if k[1] == 'sink')
            r.append(sink_sum / self.required_winners)
            if sink_sum < STRENGTH_THRESHOLD:
                return 0

        return round(r[(-1)], 9)