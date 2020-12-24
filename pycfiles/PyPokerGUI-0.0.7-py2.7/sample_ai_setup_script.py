# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/pypokergui/server/sample_ai_setup_script.py
# Compiled at: 2017-04-01 11:23:14
from pypokerengine.players import BasePokerPlayer

class FishPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        call_action_info = valid_actions[1]
        action, amount = call_action_info['action'], call_action_info['amount']
        return (action, amount)

    def receive_game_start_message(self, game_info):
        self.game_info = game_info

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return FishPlayer()