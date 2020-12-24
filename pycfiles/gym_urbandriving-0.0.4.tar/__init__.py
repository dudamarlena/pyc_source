# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jerry/Documents/drive/Projects/uds/gym_urbandriving/__init__.py
# Compiled at: 2018-04-04 17:08:52
from gym.envs.registration import register
from gym_urbandriving.envs import UrbanDrivingEnv
from gym_urbandriving.visualizer import PyGameVisualizer
from gym_urbandriving.state import PositionState
register(id='urbandriving-v0', entry_point='gym_urbandriving.envs:UrbanDrivingEnv')