# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/garl_gym/core.py
# Compiled at: 2019-05-14 13:34:29
# Size of source mod 2**32: 1348 bytes
import os, sys, numpy as np

class DiscreteWorld(object):

    def __init__(self, height, width):
        self.agents = []
        self.landmarks = []
        self.dim_p = 2
        self.dim_color = 3
        self.h = height
        self.w = width
        self.map = np.zeros((height, width))

    def gen_wall(self, prob=0, seed=10):
        if prob == 0:
            return
        np.random.seed(seed)
        for i in range(self.h):
            for j in range(self.w):
                if i == 0 or i == self.h - 1 or j == 0 or j == self.w - 1:
                    self.map[i][j] = -1
                else:
                    wall_prob = np.random.rand()
                    if wall_prob < prob:
                        self.map[i][j] = -1

    def step(self):
        raise NotImplementedError


class Agent(object):

    def __init__(self):
        self.predator = True
        self.health = None
        self.property = None
        self.pos = None
        self.random = False
        self.size = None
        self.id = None
        self.dead = False
        self.original_health = None
        self.crossover = False
        self.speed = None
        self.hunt_square = None
        self.max_reward = 0
        self.birth_time = None
        self.age = 0