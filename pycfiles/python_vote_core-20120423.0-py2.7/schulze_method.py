# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/schulze_method.py
# Compiled at: 2012-04-23 20:44:12
from schulze_helper import SchulzeHelper
from condorcet import CondorcetSystem

class SchulzeMethod(CondorcetSystem, SchulzeHelper):

    def __init__(self, ballots, tie_breaker=None, ballot_notation=None):
        super(SchulzeMethod, self).__init__(ballots, tie_breaker=tie_breaker, ballot_notation=ballot_notation)

    def as_dict(self):
        data = super(SchulzeMethod, self).as_dict()
        if hasattr(self, 'actions'):
            data['actions'] = self.actions
        return data