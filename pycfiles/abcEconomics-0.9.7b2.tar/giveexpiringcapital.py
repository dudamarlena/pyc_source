# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/giveexpiringcapital.py
# Compiled at: 2017-06-19 13:03:09
from __future__ import division
from __future__ import print_function
import abce
from abce.agents import Firm

class GiveExpiringCapital(abce.Agent, Firm):

    def init(self, simulation_parameters, _):
        self.last_round = simulation_parameters['rounds'] - 1
        if self.id == 0:
            self.create('xcapital', 10)
            assert self.possession('xcapital') == 10, self.possession('xcapital')

    def one(self):
        if self.id == 0:
            assert self.possession('xcapital') == 10, self.possession('xcapital')
            self.give('giveexpiringcapital', 1, 'xcapital', 10)
            assert self.possession('xcapital') == 0, self.possession('xcapital')

    def two(self):
        if self.id == 1:
            assert self.possession('xcapital') == 10, self.possession('xcapital')
            self.give('giveexpiringcapital', 0, 'xcapital', 10)
            assert self.possession('xcapital') == 0, self.possession('xcapital')

    def three(self):
        pass

    def clean_up(self):
        pass

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            print('Give ExpiringCapital \tOK')