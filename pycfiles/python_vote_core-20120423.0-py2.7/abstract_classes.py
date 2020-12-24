# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/abstract_classes.py
# Compiled at: 2012-04-23 20:44:09
from tie_breaker import TieBreaker
from abc import ABCMeta, abstractmethod
from copy import copy, deepcopy
import types

class VotingSystem(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, tie_breaker=None):
        self.ballots = ballots
        for ballot in self.ballots:
            if 'count' not in ballot:
                ballot['count'] = 1

        self.tie_breaker = tie_breaker
        if type(self.tie_breaker) == types.ListType:
            self.tie_breaker = TieBreaker(self.tie_breaker)
        self.calculate_results()

    @abstractmethod
    def as_dict(self):
        data = dict()
        data['candidates'] = self.candidates
        if self.tie_breaker and self.tie_breaker.ties_broken:
            data['tie_breaker'] = self.tie_breaker.as_list()
        return data

    def break_ties(self, tied_objects, reverse_order=False):
        if self.tie_breaker == None:
            self.tie_breaker = TieBreaker(self.candidates)
        return self.tie_breaker.break_ties(tied_objects, reverse_order)


class FixedWinnerVotingSystem(VotingSystem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, tie_breaker=None):
        super(FixedWinnerVotingSystem, self).__init__(ballots, tie_breaker)

    def as_dict(self):
        data = super(FixedWinnerVotingSystem, self).as_dict()
        if hasattr(self, 'tied_winners'):
            data['tied_winners'] = self.tied_winners
        return data


class MultipleWinnerVotingSystem(FixedWinnerVotingSystem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, tie_breaker=None, required_winners=1):
        self.required_winners = required_winners
        super(MultipleWinnerVotingSystem, self).__init__(ballots, tie_breaker)

    def calculate_results(self):
        if self.required_winners == len(self.candidates):
            self.winners = self.candidates

    def as_dict(self):
        data = super(MultipleWinnerVotingSystem, self).as_dict()
        data['winners'] = self.winners
        return data


class SingleWinnerVotingSystem(FixedWinnerVotingSystem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, tie_breaker=None):
        super(SingleWinnerVotingSystem, self).__init__(ballots, tie_breaker)

    def as_dict(self):
        data = super(SingleWinnerVotingSystem, self).as_dict()
        data['winner'] = self.winner
        return data


class AbstractSingleWinnerVotingSystem(SingleWinnerVotingSystem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, multiple_winner_class, tie_breaker=None):
        self.multiple_winner_class = multiple_winner_class
        super(AbstractSingleWinnerVotingSystem, self).__init__(ballots, tie_breaker=tie_breaker)

    def calculate_results(self):
        self.multiple_winner_instance = self.multiple_winner_class(self.ballots, tie_breaker=self.tie_breaker, required_winners=1)
        self.__dict__.update(self.multiple_winner_instance.__dict__)
        self.winner = list(self.winners)[0]
        del self.winners

    def as_dict(self):
        data = super(AbstractSingleWinnerVotingSystem, self).as_dict()
        data.update(self.multiple_winner_instance.as_dict())
        del data['winners']
        return data


class OrderingVotingSystem(VotingSystem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, tie_breaker=None, winner_threshold=None):
        self.winner_threshold = winner_threshold
        super(OrderingVotingSystem, self).__init__(ballots, tie_breaker=tie_breaker)

    def as_dict(self):
        data = super(OrderingVotingSystem, self).as_dict()
        data['order'] = self.order
        return data


class AbstractOrderingVotingSystem(OrderingVotingSystem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, ballots, single_winner_class, winner_threshold=None, tie_breaker=None):
        self.single_winner_class = single_winner_class
        super(AbstractOrderingVotingSystem, self).__init__(ballots, winner_threshold=winner_threshold, tie_breaker=tie_breaker)

    def calculate_results(self):
        self.order = []
        self.rounds = []
        remaining_ballots = deepcopy(self.ballots)
        remaining_candidates = True
        while (remaining_candidates == True or len(remaining_candidates) > 1) and (self.winner_threshold == None or len(self.order) < self.winner_threshold):
            result = self.single_winner_class(deepcopy(remaining_ballots), tie_breaker=self.tie_breaker)
            r = {'winner': result.winner}
            self.order.append(r['winner'])
            if hasattr(result, 'tie_breaker'):
                self.tie_breaker = result.tie_breaker
                if hasattr(result, 'tied_winners'):
                    r['tied_winners'] = result.tied_winners
            self.rounds.append(r)
            if remaining_candidates == True:
                self.candidates = result.candidates
                remaining_candidates = copy(self.candidates)
            remaining_candidates.remove(result.winner)
            remaining_ballots = self.ballots_without_candidate(result.ballots, result.winner)

        if self.winner_threshold == None or len(self.order) < self.winner_threshold:
            r = {'winner': list(remaining_candidates)[0]}
            self.order.append(r['winner'])
            self.rounds.append(r)
        return

    def as_dict(self):
        data = super(AbstractOrderingVotingSystem, self).as_dict()
        data['rounds'] = self.rounds
        return data