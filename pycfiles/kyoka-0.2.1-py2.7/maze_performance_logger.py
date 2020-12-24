# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sample/maze/maze_performance_logger.py
# Compiled at: 2016-10-04 20:35:46
from kyoka.callback.base_callback import BaseCallback
from sample.maze.maze_helper import MazeHelper

class MazePerformanceLogger(BaseCallback):

    def before_gpi_start(self, domain, value_function):
        self.step_log = []
        self.policy_log = []

    def after_update(self, iteration_count, domain, value_function, delta):
        step_to_goal = MazeHelper.measure_performance(domain, value_function)
        self.step_log.append(step_to_goal)
        self.policy_log.append(MazeHelper.visualize_policy(domain, value_function))