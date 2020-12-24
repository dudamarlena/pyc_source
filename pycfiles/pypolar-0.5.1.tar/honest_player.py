# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/examples/players/honest_player.py
# Compiled at: 2017-02-24 01:40:03
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
NB_SIMULATION = 1000

class HonestPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(nb_simulation=NB_SIMULATION, nb_player=self.nb_player, hole_card=gen_cards(hole_card), community_card=gen_cards(community_card))
        if win_rate >= 1.0 / self.nb_player:
            action = valid_actions[1]
        else:
            action = valid_actions[0]
        return (action['action'], action['amount'])

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass