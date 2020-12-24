# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/irv.py
# Compiled at: 2012-04-23 20:44:12
from abstract_classes import AbstractSingleWinnerVotingSystem
from stv import STV

class IRV(AbstractSingleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None):
        super(IRV, self).__init__(ballots, STV, tie_breaker=tie_breaker)

    def calculate_results(self):
        super(IRV, self).calculate_results()
        IRV.singularize(self.rounds)

    def as_dict(self):
        data = super(IRV, self).as_dict()
        IRV.singularize(data['rounds'])
        return data

    @staticmethod
    def singularize(rounds):
        for r in rounds:
            if 'winners' in r:
                r['winner'] = list(r['winners'])[0]
                del r['winners']