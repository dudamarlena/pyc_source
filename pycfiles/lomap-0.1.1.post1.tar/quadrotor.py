# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alphan/Documents/svn/academic/bu/research/implementation/lomap-ltl_optimal_multi-agent_planner/trunk/examples/ijrr2014_rec_hor/quadrotor.py
# Compiled at: 2015-04-14 16:40:40
import itertools as it, lomap, logging
logger = logging.getLogger(__name__)

class Quadrotor:

    def __init__(self, env, x, y, sensing_range):
        self.env = env
        self.x, self.y = x, y
        assert sensing_range % 2 == 1, "sensing_range must be an odd value, '%d' is not odd!" % sensing_range
        self.sensing_range = sensing_range
        self.cmds = {'n': 'self.y += 1', 'e': 'self.x += 1', 's': 'self.y -= 1', 'w': 'self.x -= 1', 'h': ''}
        self.sense()

    def get_sensing_cell_global_coords(self, cell):
        cx, cy = cell
        assert cx >= 0 and cy >= 0
        return (cx - self.sensing_range / 2 + self.x, cy - self.sensing_range / 2 + self.y)

    def sense(self):
        self.sensed = [ [ {'local_reqs': set([]), 'global_reqs': set([])} for y in range(0, self.sensing_range) ] for x in range(0, self.sensing_range) ]
        for cx, cy in it.product(range(0, self.sensing_range), repeat=2):
            x, y = self.get_sensing_cell_global_coords((cx, cy))
            if (
             x, y) in self.env.local_reqs and self.env.local_reqs[(x, y)]['on']:
                self.sensed[cx][cy]['local_reqs'] = self.env.local_reqs[(x, y)]['reqs']
            if (x, y) in self.env.global_reqs:
                self.sensed[cx][cy]['global_reqs'] = self.env.global_reqs[(x, y)]['reqs']

    def move_quad(self, cmd):
        exec self.cmds[cmd]
        self.sense()