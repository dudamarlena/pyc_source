# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/sample/ticktacktoe/ticktacktoe_keras_value_function_test.py
# Compiled at: 2016-10-26 09:22:48
from tests.base_unittest import BaseUnitTest

class TickTackToeKerasValueFunctioneXtest(BaseUnitTest):

    def setUp(self):
        self.func = TickTackToeKerasValueFunction()
        self.func.setUp()

    def xtest_state_action_into_input(self):
        bin2i = lambda b: int(b, 2)
        first_player_board = bin2i('000000100')
        second_player_board = bin2i('000000010')
        action = 1
        model_input = self.func.transform_state_action_into_input((first_player_board, second_player_board), action)
        self.eq([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], model_input)

    def xtest_prediction(self):
        bin2i = lambda b: int(b, 2)
        first_player_board = bin2i('000000100')
        second_player_board = bin2i('000000010')
        state = (first_player_board, second_player_board)
        action = 1
        model_input = self.func.transform_state_action_into_input((first_player_board, second_player_board), action)
        delta = self.func.update_function(state, action, 0)
        res = self.func.calculate_value(state, action)
        self.debug()