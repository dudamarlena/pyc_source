# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/deepq/experiments/train_mountaincar.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 658 bytes
import gym
from deephyper.search.nas.baselines import deepq
from deephyper.search.nas.baselines.common import models

def main():
    env = gym.make('MountainCar-v0')
    act = deepq.learn(env,
      network=models.mlp(num_hidden=64, num_layers=1),
      lr=0.001,
      total_timesteps=100000,
      buffer_size=50000,
      exploration_fraction=0.1,
      exploration_final_eps=0.1,
      print_freq=10,
      param_noise=True)
    print('Saving model to mountaincar_model.pkl')
    act.save('mountaincar_model.pkl')


if __name__ == '__main__':
    main()