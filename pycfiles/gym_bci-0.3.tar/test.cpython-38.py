# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/gym_bci/envs/test.py
# Compiled at: 2019-11-23 13:53:43
# Size of source mod 2**32: 379 bytes
import gym, gym_bci, time, logging, random
logging.getLogger().setLevel(logging.INFO)
env = gym.make('bci-arrows-v0')
environ_config = {'maintain':500, 
 'min_delay':20, 
 'max_delay':80}
(env.reset)(**environ_config)
actions = [
 'right', 'left', 'south', 'north']
for i in range(100):
    env.step(random.choice(actions))
else:
    env.close()