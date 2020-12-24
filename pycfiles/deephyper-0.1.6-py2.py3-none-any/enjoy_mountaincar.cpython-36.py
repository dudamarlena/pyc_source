# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/deepq/experiments/enjoy_mountaincar.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 642 bytes
import gym
from deephyper.search.nas.baselines import deepq
from deephyper.search.nas.baselines.common import models

def main():
    env = gym.make('MountainCar-v0')
    act = deepq.learn(env,
      network=models.mlp(num_layers=1, num_hidden=64),
      total_timesteps=0,
      load_path='mountaincar_model.pkl')
    while True:
        obs, done = env.reset(), False
        episode_rew = 0
        while not done:
            env.render()
            obs, rew, done, _ = env.step(act(obs[None])[0])
            episode_rew += rew

        print('Episode reward', episode_rew)


if __name__ == '__main__':
    main()