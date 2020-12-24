# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/deepq/experiments/train_cartpole.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 678 bytes
import gym
from baselines import deepq

def callback(lcl, _glb):
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved


def main():
    env = gym.make('CartPole-v0')
    model = deepq.models.mlp([64])
    act = deepq.learn(env, q_func=model, lr=0.001, max_timesteps=100000, buffer_size=50000, exploration_fraction=0.1, exploration_final_eps=0.02, print_freq=10, callback=callback)
    print('Saving model to cartpole_model.pkl')
    act.save('cartpole_model.pkl')


if __name__ == '__main__':
    main()