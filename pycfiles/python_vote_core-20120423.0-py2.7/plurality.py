# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/plurality.py
# Compiled at: 2012-04-23 20:44:14
from abstract_classes import AbstractSingleWinnerVotingSystem
from plurality_at_large import PluralityAtLarge

class Plurality(AbstractSingleWinnerVotingSystem):

    def __init__(self, ballots, tie_breaker=None):
        super(Plurality, self).__init__(ballots, PluralityAtLarge, tie_breaker=tie_breaker)