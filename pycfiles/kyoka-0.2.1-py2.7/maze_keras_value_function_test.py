# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/sample/maze/maze_keras_value_function_test.py
# Compiled at: 2016-10-26 09:22:48
import os
from tests.base_unittest import BaseUnitTest
from sample.maze.maze_domain import MazeDomain

class MazeKerasValueFunctionTest(BaseUnitTest):

    def setUp(self):
        self.domain = MazeDomain()
        self.domain.read_maze(self.__get_sample_maze_path())
        self.func = MazeKerasValueFunction(self.domain)
        self.func.setUp()

    def xtest_transform_state_action_into_input(self):
        test_func = lambda state, action: self.func.transform_state_action_into_input(state, action)
        state1, action1 = (0, 0), self.domain.RIGHT
        self.eq([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], test_func(state1, action1))
        state2, action2 = (2, 1), self.domain.UP
        self.eq([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], test_func(state2, action2))

    def xtest_prediction(self):
        state, action = (0, 0), self.domain.DOWN
        delta = self.func.update_function(state, action, 1)
        res = self.func.calculate_value(state, action)
        self.debug()

    def __get_sample_maze_path(self):
        return os.path.join(os.path.dirname(__file__), 'sample_maze.txt')