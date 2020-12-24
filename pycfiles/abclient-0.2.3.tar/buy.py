# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abcEconomics/unittest/buy.py
# Compiled at: 2018-05-10 08:13:51
from __future__ import division
from __future__ import print_function
import random
from abcEconomics.agent import Agent
from abcEconomics import NotEnoughGoods
from tools import is_zero

class Buy(Agent):

    def init(self, rounds):
        self.last_round = rounds - 1
        self.tests = {'accepted': False, 'rejected': False, 'partial': False}
        self.price = 0
        if self.id == 1:
            self.tests['not_answered'] = False

    def one(self):
        """ Acts only if he is agent 0: sends an buy offer to agent 1 offer
        """
        if self.id % 2 == 0:
            self.create('money', random.uniform(0, 10000))
            self.money = self['money']
            self.price = random.uniform(0.0001, 1)
            quantity = random.uniform(0, self.money / self.price)
            self.offer = self.make_bid(('buy', self.id + 1), 'cookies', quantity, self.price)
            assert self.not_reserved('money') == self.money - quantity * self.price

    def two(self):
        """ Acts only if he is agent 1: recieves offers and accepts;
        rejects; partially accepts and leaves offers unanswerd.
        """
        if self.id % 2 == 1:
            self.create('cookies', random.uniform(0, 10000))
            cookies = self['cookies']
            oo = self.get_bids('cookies')
            assert oo
            for offer in oo:
                if random.randint(0, 10) == 0:
                    self.tests['not_answered'] = True
                    continue
                else:
                    if random.randint(0, 10) == 0:
                        self.reject(offer)
                        assert self['money'] == 0
                        assert self['cookies'] == cookies
                        self.tests['rejected'] = True
                        break
                    try:
                        self.accept(offer)
                        assert self['money'] == offer.price * offer.quantity
                        assert self['cookies'] == cookies - offer.quantity
                        self.tests['accepted'] = True
                    except NotEnoughGoods:
                        self.accept(offer, self['cookies'])
                        assert is_zero(self['cookies'])
                        assert self['money'] == cookies * offer.price
                        self.tests['partial'] = True

    def three(self):
        """
        """
        if self.id % 2 == 0:
            offer = self.offer
            if offer.status == 'rejected':
                test = self.money - self['money']
                assert is_zero(test), test
                self.tests['rejected'] = True
            elif offer.status == 'accepted':
                if offer.final_quantity == offer.quantity:
                    assert self.money - offer.quantity * offer.price == self['money']
                    assert self['cookies'] == offer.quantity
                    self.tests['accepted'] = True
                else:
                    test = self.money - offer.final_quantity * offer.price - self['money']
                    assert is_zero(test), test
                    test = self['cookies'] - offer.final_quantity
                    assert is_zero(test), test
                    self.tests['partial'] = True
            else:
                SystemExit('Error in buy')

    def laut(self):
        print('laut')
        self.haut = 'xxxx'

    def clean_up(self):
        self.destroy('money')
        self.destroy('cookies')

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            assert all(self.tests.values()), 'not all tests have been run; ABCE workes correctly, restart the unittesting to do all tests %s' % self.tests
            print('Test abcEconomics.buy:\t\t\t\t\tOK')
            print('Test abcEconomics.accept\t(abcEconomics.buy):\t\tOK')
            print('Test abcEconomics.reject\t(abcEconomics.buy):\t\tOK')
            print('Test abcEconomics.accept, partial\t(abcEconomics.buy):\tOK')
            print('Test reject pending automatic \t(abcEconomics.buy):\tOK')