# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/examples/players/fish_player.py
# Compiled at: 2016-11-22 02:08:34
from pypokerengine.players import BasePokerPlayer

class FishPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        call_action_info = valid_actions[1]
        action, amount = call_action_info['action'], call_action_info['amount']
        return (
         action, amount)

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass