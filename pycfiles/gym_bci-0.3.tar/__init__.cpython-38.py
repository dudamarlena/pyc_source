# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/gym_bci/__init__.py
# Compiled at: 2019-11-23 17:07:29
# Size of source mod 2**32: 201 bytes
from gym.envs.registration import register
register(id='bci-arrows-v0',
  entry_point='gym_bci.envs:ArrowsEnv')
register(id='bci-pacman-v0',
  entry_point='gym_bci.envs:PacmanEnv')