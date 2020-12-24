# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sample/maze/maze_transformer.py
# Compiled at: 2016-09-22 09:06:48
from kyoka.callback.base_callback import BaseCallback
import logging

class MazeTransformer(BaseCallback):

    def __init__(self):
        BaseCallback.__init__(self)
        self.transformation = {}

    def set_transformation(self, timing, maze_path):
        self.transformation[timing] = maze_path

    def before_update(self, iteration_count, domain, value_function):
        if iteration_count in self.transformation:
            maze_filepath = self.transformation[iteration_count]
            domain.read_maze(maze_filepath)
            logging.debug('Maze transformed into [ %s ]' % maze_filepath)