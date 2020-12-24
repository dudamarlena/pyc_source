# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/holdem/__init__.py
# Compiled at: 2018-01-07 14:40:09
# Size of source mod 2**32: 532 bytes
from gym.envs.registration import register
from .env import TexasHoldemEnv
from .utils import card_to_str, hand_to_str, safe_actions, action_table
register(id='TexasHoldem-v0',
  entry_point='holdem.env:TexasHoldemEnv',
  kwargs={'n_seats':2, 
 'debug':False})
register(id='TexasHoldem-v1',
  entry_point='holdem.env:TexasHoldemEnv',
  kwargs={'n_seats':4, 
 'debug':False})
register(id='TexasHoldem-v2',
  entry_point='holdem.env:TexasHoldemEnv',
  kwargs={'n_seats':8, 
 'debug':False})