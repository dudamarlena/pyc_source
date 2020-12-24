# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/pypokerengine/engine/sidepot_test.py
# Compiled at: 2016-11-29 05:14:24
from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.player import Player
from pypokerengine.engine.pay_info import PayInfo
from pypokerengine.engine.game_evaluator import GameEvaluator

class SidepotTest(BaseUnitTest):
    """ A: $50, B: $20(ALLIN),  C: $30(ALLIN) """

    def test_case1(self):
        players = {'A': self.__create_player_with_pay_info('A', 50, PayInfo.PAY_TILL_END), 
           'B': self.__create_player_with_pay_info('B', 20, PayInfo.ALLIN), 
           'C': self.__create_player_with_pay_info('C', 30, PayInfo.ALLIN)}
        pots = GameEvaluator.create_pot(players.values())
        self.eq(3, len(pots))
        self.__sidepot_check(players, pots[0], 60, ['A', 'B', 'C'])
        self.__sidepot_check(players, pots[1], 20, ['A', 'C'])
        self.__sidepot_check(players, pots[2], 20, ['A'])

    def test_case2(self):
        players = {'A': self.__create_player_with_pay_info('A', 10, PayInfo.PAY_TILL_END), 
           'B': self.__create_player_with_pay_info('B', 10, PayInfo.PAY_TILL_END), 
           'C': self.__create_player_with_pay_info('C', 7, PayInfo.ALLIN)}
        pots = GameEvaluator.create_pot(players.values())
        self.eq(2, len(pots))
        self.__sidepot_check(players, pots[0], 21, ['A', 'B', 'C'])
        self.__sidepot_check(players, pots[1], 6, ['A', 'B'])

    def test_case3(self):
        players = {'A': self.__create_player_with_pay_info('A', 20, PayInfo.FOLDED), 
           'B': self.__create_player_with_pay_info('B', 30, PayInfo.PAY_TILL_END), 
           'C': self.__create_player_with_pay_info('C', 7, PayInfo.ALLIN), 
           'D': self.__create_player_with_pay_info('D', 30, PayInfo.PAY_TILL_END)}
        pots = GameEvaluator.create_pot(players.values())
        self.eq(2, len(pots))
        self.__sidepot_check(players, pots[0], 28, ['B', 'C', 'D'])
        self.__sidepot_check(players, pots[1], 59, ['B', 'D'])

    def test_case4(self):
        players = {'A': self.__create_player_with_pay_info('A', 12, PayInfo.ALLIN), 
           'B': self.__create_player_with_pay_info('B', 30, PayInfo.PAY_TILL_END), 
           'C': self.__create_player_with_pay_info('C', 7, PayInfo.ALLIN), 
           'D': self.__create_player_with_pay_info('D', 30, PayInfo.PAY_TILL_END)}
        pots = GameEvaluator.create_pot(players.values())
        self.eq(3, len(pots))
        self.__sidepot_check(players, pots[0], 28, ['A', 'B', 'C', 'D'])
        self.__sidepot_check(players, pots[1], 15, ['A', 'B', 'D'])
        self.__sidepot_check(players, pots[2], 36, ['B', 'D'])

    def test_case5(self):
        players = {'A': self.__create_player_with_pay_info('A', 5, PayInfo.ALLIN), 
           'B': self.__create_player_with_pay_info('B', 10, PayInfo.PAY_TILL_END), 
           'C': self.__create_player_with_pay_info('C', 8, PayInfo.ALLIN), 
           'D': self.__create_player_with_pay_info('D', 10, PayInfo.PAY_TILL_END), 
           'E': self.__create_player_with_pay_info('E', 2, PayInfo.FOLDED)}
        pots = GameEvaluator.create_pot(players.values())
        self.eq(3, len(pots))
        self.__sidepot_check(players, pots[0], 22, ['A', 'B', 'C', 'D'])
        self.__sidepot_check(players, pots[1], 9, ['B', 'C', 'D'])
        self.__sidepot_check(players, pots[2], 4, ['B', 'D'])

    def __create_player_with_pay_info(self, name, amount, status):
        player = Player('uuid', 100, name)
        player.pay_info.amount = amount
        player.pay_info.status = status
        return player

    def __sidepot_check(self, players, pot, amount, eligibles):
        self.eq(amount, pot['amount'])
        self.eq(len(eligibles), len(pot['eligibles']))
        for name in eligibles:
            self.true(players[name] in pot['eligibles'])