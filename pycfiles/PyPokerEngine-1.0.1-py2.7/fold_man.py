# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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