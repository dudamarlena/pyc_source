# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/deepq/experiments/train_mountaincar.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 595 bytes
import gym
from baselines import deepq

def main():
    env = gym.make('MountainCar-v0')
    model = deepq.models.mlp([64], layer_norm=True)
    act = deepq.learn(env, q_func=model, lr=0.001, max_timesteps=100000, buffer_size=50000, exploration_fraction=0.1, exploration_final_eps=0.1, print_freq=10, param_noise=True)
    print('Saving model to mountaincar_model.pkl')
    act.save('mountaincar_model.pkl')


if __name__ == '__main__':
    main()