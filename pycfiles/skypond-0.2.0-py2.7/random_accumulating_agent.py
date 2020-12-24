# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/four_keys/agents/random_accumulating_agent.py
# Compiled at: 2019-05-01 21:43:12
from __future__ import absolute_import
from ...base.base_agent import Agent
from skypond.games.four_keys.four_keys_actions import FourKeysActions
import numpy as np

class RandomAccumulatingAgent(Agent):

    def __init__(self, name='random'):
        super().__init__()
        self.name = name
        self.blind = True

    def react(self, observation):
        action = np.random.choice([FourKeysActions.UP, FourKeysActions.DOWN, FourKeysActions.LEFT, FourKeysActions.RIGHT, FourKeysActions.ATTACK])
        return action

    def describe(self):
        return {'username': self.name, 'eth_address': '', 'email': 'test@example.com', 'description': 'Sample Random Agent'}