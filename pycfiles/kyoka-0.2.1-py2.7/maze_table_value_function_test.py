# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/sample/maze/maze_table_value_function_test.py
# Compiled at: 2016-10-18 21:59:44
from tests.base_unittest import BaseUnitTest
from sample.maze.maze_table_value_function import MazeTableValueFunction

class MazeTableValueFunctionTest(BaseUnitTest):

    def setUp(self):
        self.func = MazeTableValueFunction(maze_shape=(3, 4))
        self.func.setUp()

    def test_generate_initial_table(self):
        table = self.func.generate_initial_table()
        self.eq(3, len(table))
        self.eq(4, len(table[0]))
        self.eq(4, len(table[0][0]))
        self.eq(0, table[0][0][0])

    def test_calculate_value(self):
        state = (1, 3)
        action = 2
        self.func.table[1][3][2] = 1
        self.eq(1, self.func.calculate_value(state, action))

    def test_update_function(self):
        bin2i = lambda b: int(b, 2)
        first_player_board = bin2i('000000100')
        second_player_board = bin2i('000000010')
        state = (2, 3)
        action = 1
        self.eq(0, self.func.calculate_value(state, action))
        self.func.update_function(state, action, 1)
        self.eq(1, self.func.calculate_value(state, action))
        self.func.update_function(state, action, 0)
        self.eq(0, self.func.calculate_value(state, action))