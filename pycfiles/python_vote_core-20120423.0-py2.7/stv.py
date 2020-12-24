# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/stv.py
# Compiled at: 2012-04-23 20:44:10
from abstract_classes import MultipleWinnerVotingSystem
import math, copy
from common_functions import matching_keys

class STV(MultipleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None, required_winners=1):
        super(STV, self).__init__(ballots, tie_breaker=tie_breaker, required_winners=required_winners)

    def calculate_results(self):
        self.candidates = set()
        for ballot in self.ballots:
            ballot['count'] = float(ballot['count'])
            self.candidates.update(set(ballot['ballot']))

        self.quota = STV.droop_quota(self.ballots, self.required_winners)
        self.rounds = []
        self.winners = set()
        quota = self.quota
        remaining_candidates = copy.deepcopy(self.candidates)
        ballots = copy.deepcopy(self.ballots)
        while len(self.winners) < self.required_winners and len(remaining_candidates) + len(self.winners) > self.required_winners:
            round = {}
            if len(filter(lambda ballot: ballot['count'] > 0, ballots)) == 0:
                round['note'] = 'reset'
                ballots = copy.deepcopy(self.ballots)
                for ballot in ballots:
                    ballot['ballot'] = filter(lambda x: x in remaining_candidates, ballot['ballot'])

                quota = STV.droop_quota(ballots, self.required_winners - len(self.winners))
            round['tallies'] = STV.tallies(ballots)
            if max(round['tallies'].values()) >= quota:
                round['winners'] = set([ candidate for candidate, tally in round['tallies'].items() if tally >= self.quota
                                       ])
                self.winners |= round['winners']
                remaining_candidates -= round['winners']
                for ballot in ballots:
                    if ballot['ballot'][0] in round['winners']:
                        ballot['count'] *= (round['tallies'][ballot['ballot'][0]] - self.quota) / round['tallies'][ballot['ballot'][0]]

                ballots = self.remove_candidates_from_ballots(round['winners'], ballots)
            else:
                round.update(self.loser(round['tallies']))
                remaining_candidates.remove(round['loser'])
                ballots = self.remove_candidates_from_ballots([round['loser']], ballots)
            self.rounds.append(round)

        if len(self.winners) < self.required_winners:
            self.remaining_candidates = remaining_candidates
            self.winners |= self.remaining_candidates

    def as_dict(self):
        data = super(STV, self).as_dict()
        data['quota'] = self.quota
        data['rounds'] = self.rounds
        if hasattr(self, 'remaining_candidates'):
            data['remaining_candidates'] = self.remaining_candidates
        return data

    def loser(self, tallies):
        losers = matching_keys(tallies, min(tallies.values()))
        if len(losers) == 1:
            return {'loser': list(losers)[0]}
        else:
            return {'tied_losers': losers, 
               'loser': self.break_ties(losers, True)}

    @staticmethod
    def remove_candidates_from_ballots(candidates, ballots):
        for ballot in ballots:
            for candidate in candidates:
                if candidate in ballot['ballot']:
                    ballot['ballot'].remove(candidate)

        return ballots

    @staticmethod
    def tallies(ballots):
        tallies = dict.fromkeys(STV.viable_candidates(ballots), 0)
        for ballot in ballots:
            if len(ballot['ballot']) > 0:
                tallies[ballot['ballot'][0]] += ballot['count']

        return dict((candidate, votes) for candidate, votes in tallies.iteritems() if votes > 0)

    @staticmethod
    def viable_candidates(ballots):
        candidates = set([])
        for ballot in ballots:
            candidates |= set(ballot['ballot'])

        return candidates

    @staticmethod
    def droop_quota(ballots, seats=1):
        voters = 0
        for ballot in ballots:
            voters += ballot['count']

        return int(math.floor(voters / (seats + 1)) + 1)