# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/four_keys/agents/random_agent.py
# Compiled at: 2019-05-07 01:29:13
from __future__ import absolute_import
from ...base.base_agent import Agent
import numpy as np
from skypond.games.four_keys.four_keys_actions import FourKeysActions

class RandomAgent(Agent):

    def __init__(self, name='random'):
        super().__init__()
        self.name = name
        self.blind = True

    def react(self, observation):
        return np.random.randint(0, len(FourKeysActions))

    def describe(self):
        return {'username': self.name, 'eth_address': '', 'email': 'test@example.com', 'description': 'Sample Random Agent'}