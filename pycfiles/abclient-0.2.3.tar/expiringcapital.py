# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/expiringcapital.py
# Compiled at: 2017-06-19 13:03:09
from __future__ import division
from __future__ import print_function
import abce
from abce.agents import Firm

class ExpiringCapital(abce.Agent, Firm):

    def init(self, simulation_parameters, _):
        self.last_round = simulation_parameters['rounds'] - 1
        self.create('xcapital', 1)
        print('============', self.simulation_parameters['xcapital'])

    def one(self):
        pass

    def two(self):
        pass

    def three(self):
        pass

    def go(self):
        if self.round == 2:
            self.create('xcapital', 10)
        if self.round == 0:
            assert self.possession('xcapital') == 1
            assert self.round == 1 and self.possession('xcapital') == 1
        if self.round == 2:
            assert self.possession('xcapital') == 11
            assert self.round == 3 and self.possession('xcapital') == 11
        if self.round == 4:
            assert self.possession('xcapital') == 11
            assert self.round == 5 and self.possession('xcapital') == 10

    def clean_up(self):
        pass

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            print('simple ExpiringCapital \tOK')