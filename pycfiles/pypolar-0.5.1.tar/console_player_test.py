# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/examples/players/console_player_test.py
# Compiled at: 2016-11-22 02:08:34
from tests.base_unittest import BaseUnitTest
from examples.players.console_player import ConsolePlayer

class ConsolePlayerTest(BaseUnitTest):

    def setUp(self):
        self.valid_actions = [{'action': 'fold', 'amount': 0}, {'action': 'call', 'amount': 10}, {'action': 'raise', 'amount': {'max': 105, 'min': 15}}]
        self.round_state = {'dealer_btn': 1, 
           'street': 'preflop', 
           'seats': [{'stack': 85, 'state': 'participating', 'name': 'player1', 'uuid': 'ciglbcevkvoqzguqvnyhcb'}, {'stack': 100, 'state': 'participating', 'name': 'player2', 'uuid': 'zjttlanhlvpqzebrwmieho'}], 'next_player': 1, 
           'small_blind_pos': 0, 
           'big_blind_pos': 1, 
           'community_card': [], 'pot': {'main': {'amount': 15}, 'side': []}, 'round_count': 3, 
           'action_histories': {'preflop': [{'action': 'SMALLBLIND', 'amount': 5, 'add_amount': 5, 'uuid': 'ciglbcevkvoqzguqvnyhcb'}, {'action': 'BIGBLIND', 'amount': 10, 'add_amount': 5, 'uuid': 'zjttlanhlvpqzebrwmieho'}]}}

    def test_declare_fold(self):
        mock_input = self.__gen_raw_input_mock(['f'])
        player = ConsolePlayer(mock_input)
        player.set_uuid('dummy')
        action, amount = player.declare_action(self.valid_actions, None, self.round_state)
        self.eq('fold', action)
        self.eq(0, amount)
        return

    def test_declare_call(self):
        mock_input = self.__gen_raw_input_mock(['c'])
        player = ConsolePlayer(mock_input)
        player.set_uuid('dummy')
        action, amount = player.declare_action(self.valid_actions, None, self.round_state)
        self.eq('call', action)
        self.eq(10, amount)
        return

    def test_declare_valid_raise(self):
        mock_input = self.__gen_raw_input_mock(['r', '15'])
        player = ConsolePlayer(mock_input)
        player.set_uuid('dummy')
        action, amount = player.declare_action(self.valid_actions, None, self.round_state)
        self.eq('raise', action)
        self.eq(15, amount)
        return

    def test_correct_invalid_raise(self):
        mock_input = self.__gen_raw_input_mock(['r', '14', '105'])
        player = ConsolePlayer(mock_input)
        player.set_uuid('dummy')
        action, amount = player.declare_action(self.valid_actions, None, self.round_state)
        self.eq('raise', action)
        self.eq(105, amount)
        return

    def __gen_raw_input_mock(self, mock_returns):
        counter = []

        def raw_input_wrapper(self):
            mock_return = mock_returns[len(counter)]
            counter.append(0)
            return mock_return

        return raw_input_wrapper