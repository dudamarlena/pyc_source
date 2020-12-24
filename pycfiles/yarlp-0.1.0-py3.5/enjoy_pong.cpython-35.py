# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/deepq/experiments/enjoy_pong.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 474 bytes
import gym
from baselines import deepq

def main():
    env = gym.make('PongNoFrameskip-v4')
    env = deepq.wrap_atari_dqn(env)
    act = deepq.load('pong_model.pkl')
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