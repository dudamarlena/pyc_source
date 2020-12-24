# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/schulze_npr.py
# Compiled at: 2012-04-23 20:44:06
from abstract_classes import AbstractOrderingVotingSystem
from schulze_helper import SchulzeHelper
from schulze_method import SchulzeMethod

class SchulzeNPR(AbstractOrderingVotingSystem, SchulzeHelper):

    def __init__(self, ballots, winner_threshold=None, tie_breaker=None, ballot_notation=None):
        self.standardize_ballots(ballots, ballot_notation)
        super(SchulzeNPR, self).__init__(self.ballots, single_winner_class=SchulzeMethod, winner_threshold=winner_threshold, tie_breaker=tie_breaker)

    @staticmethod
    def ballots_without_candidate(ballots, candidate):
        for ballot in ballots:
            if candidate in ballot['ballot']:
                del ballot['ballot'][candidate]

        return ballots