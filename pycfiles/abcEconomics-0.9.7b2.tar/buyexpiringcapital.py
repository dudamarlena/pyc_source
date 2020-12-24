# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/buyexpiringcapital.py
# Compiled at: 2017-12-13 07:05:30
from __future__ import division
from __future__ import print_function
import abce
from abce.agents import Firm

class BuyExpiringCapital(abce.Agent, Firm):

    def init(self, rounds):
        self.last_round = rounds - 1

    def one(self):
        if self.id == 0:
            self.create('money', 10)
            self.buy('buyexpiringcapital', 1, good='xcapital', quantity=10, price=1)
            assert self.free('xcapital') == 0
            assert self.free('money') == 0

    def two(self):
        if self.id == 1:
            self.create('xcapital', 10)
            assert self['xcapital'] == 10
            assert self['money'] == 0
            offer = self.get_offers('xcapital')[0]
            self['xcapital'] == 10
            self.accept(offer)
            assert self['xcapital'] == 0
            assert self['money'] == 10

    def three(self):
        if self.id == 0:
            assert self['xcapital'] == 10
            self.destroy('xcapital', 10)
        elif self.id == 1:
            assert self['money'] == 10
            self.destroy('money', 10)

    def clean_up(self):
        pass

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            print('BuyExpiringCapital \tOK')