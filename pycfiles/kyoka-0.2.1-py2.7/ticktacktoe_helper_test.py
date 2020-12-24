# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/sample/ticktacktoe/ticktacktoe_helper_test.py
# Compiled at: 2016-09-18 11:35:05
from tests.base_unittest import BaseUnitTest
from sample.ticktacktoe.ticktacktoe_helper import TickTackToeHelper

class TickTackToeHelperTest(BaseUnitTest):

    def test_visualize_board_when_empty(self):
        bin2i = lambda b: int(b, 2)
        first_player_board = bin2i('000000000')
        second_player_board = bin2i('000000000')
        state = (first_player_board, second_player_board)
        expected = '- - -\n- - -\n- - -'
        self.eq(expected, TickTackToeHelper.visualize_board(state))

    def test_visualize_board_when_not_empty(self):
        bin2i = lambda b: int(b, 2)
        first_player_board = bin2i('110000000')
        second_player_board = bin2i('000000011')
        state = (first_player_board, second_player_board)
        expected = 'O O -\n- - -\n- X X'
        self.eq(expected, TickTackToeHelper.visualize_board(state))