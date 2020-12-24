# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/engine/action_checker.py
# Compiled at: 2017-04-01 23:56:44
from functools import reduce

class ActionChecker:

    @classmethod
    def correct_action(self, players, player_pos, sb_amount, action, amount=None):
        if self.is_allin(players[player_pos], action, amount):
            amount = players[player_pos].stack + players[player_pos].paid_sum()
        elif self.__is_illegal(players, player_pos, sb_amount, action, amount):
            action, amount = ('fold', 0)
        return (action, amount)

    @classmethod
    def is_allin(self, player, action, bet_amount):
        if action == 'call':
            return bet_amount >= player.stack + player.paid_sum()
        else:
            if action == 'raise':
                return bet_amount == player.stack + player.paid_sum()
            return False

    @classmethod
    def need_amount_for_action(self, player, amount):
        return amount - player.paid_sum()

    @classmethod
    def agree_amount(self, players):
        last_raise = self.__fetch_last_raise(players)
        if last_raise:
            return last_raise['amount']
        return 0

    @classmethod
    def legal_actions(self, players, player_pos, sb_amount):
        min_raise = self.__min_raise_amount(players, sb_amount)
        max_raise = players[player_pos].stack + players[player_pos].paid_sum()
        if max_raise < min_raise:
            min_raise = max_raise = -1
        return [{'action': 'fold', 'amount': 0}, {'action': 'call', 'amount': self.agree_amount(players)}, {'action': 'raise', 'amount': {'min': min_raise, 'max': max_raise}}]

    @classmethod
    def _is_legal(self, players, player_pos, sb_amount, action, amount=None):
        return not self.__is_illegal(players, player_pos, sb_amount, action, amount)

    @classmethod
    def __is_illegal(self, players, player_pos, sb_amount, action, amount=None):
        if action == 'fold':
            return False
        if action == 'call':
            return self.__is_short_of_money(players[player_pos], amount) or self.__is_illegal_call(players, amount)
        if action == 'raise':
            return self.__is_short_of_money(players[player_pos], amount) or self.__is_illegal_raise(players, amount, sb_amount)

    @classmethod
    def __is_illegal_call(self, players, amount):
        return amount != self.agree_amount(players)

    @classmethod
    def __is_illegal_raise(self, players, amount, sb_amount):
        return self.__min_raise_amount(players, sb_amount) > amount

    @classmethod
    def __min_raise_amount(self, players, sb_amount):
        raise_ = self.__fetch_last_raise(players)
        if raise_:
            return raise_['amount'] + raise_['add_amount']
        return sb_amount * 2

    @classmethod
    def __is_short_of_money(self, player, amount):
        return player.stack < amount - player.paid_sum()

    @classmethod
    def __fetch_last_raise(self, players):
        all_histories = [ p.action_histories for p in players ]
        all_histories = reduce(lambda acc, e: acc + e, all_histories)
        raise_histories = [ h for h in all_histories if h['action'] in ('RAISE', 'SMALLBLIND',
                                                                        'BIGBLIND') ]
        if len(raise_histories) == 0:
            return
        else:
            return max(raise_histories, key=lambda h: h['amount'])
            return