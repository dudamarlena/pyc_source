# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/borda/count.py
# Compiled at: 2013-08-05 13:27:40
"""This module holds all classes necessary to implement a Borda voting
election"""
import operator

class Election(object):
    """Election of Borda votes"""

    def set_candidates(self, candidates):
        self.candidates = candidates
        self.votes = {}

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def get_winner(self):
        sorted_votes = sorted(self.votes.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_votes[0][0]

    def give_points(self, chosen, points):
        for candidate in self.candidates:
            if candidate == chosen:
                self.votes.setdefault(chosen, 0)
                self.votes[chosen] += points


class Voter(object):
    """Voter is a participant in a Borda voting"""

    def __init__(self, election, name):
        self.election = election
        self.name = name

    def votes(self, candidates):
        total = len(candidates)
        for pos, candidate in enumerate(candidates):
            points = total - pos
            self.election.give_points(candidate, points)


class Candidate(object):
    """Candidate is a candidate to be a winner in a Borda voting"""

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)