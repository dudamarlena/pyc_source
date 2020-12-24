# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/players/sample/fold_man.py
# Compiled at: 2016-09-02 07:12:43
from pypokerengine.players.base_poker_player import BasePokerPlayer

class PokerPlayer(BasePokerPlayer):

    def declare_action(self, hole_card, valid_actions, round_state, action_histories):
        return ('fold', 0)

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state, action_histories):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

    def receive_game_result_message(self, seats):
        pass