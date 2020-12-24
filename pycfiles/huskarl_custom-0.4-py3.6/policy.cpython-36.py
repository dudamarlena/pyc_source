# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/huskarl/policy.py
# Compiled at: 2019-06-13 12:59:36
# Size of source mod 2**32: 2517 bytes
import random, numpy as np
from scipy.stats import truncnorm

class Policy:
    __doc__ = 'Abstract base class for all implemented policies.\n\t\n\tDo not use this abstract base class directly but instead use one of the concrete policies implemented.\n\n\tA policy ultimately returns the action to be taken based on the output of the agent.\n\tThe policy is the place to implement action-space exploration strategies.\n\tIf the action space is discrete, the policy usually receives action values and has to pick an action/index.\n\tA discrete action-space policy can explore by pick an action at random with a small probability e.g. EpsilonGreedy.\n\tIf the action space is continuous, the policy usually receives a single action or a distribution over actions.\n\tA continuous action-space policy can simply sample from the distribution and/or add noise to the received action.\t\n\t\n\tTo implement your own policy, you have to implement the following method:\n\t'

    def act(self, **kwargs):
        raise NotImplementedError()


class Greedy(Policy):
    __doc__ = 'Greedy Policy\n\n\tThis policy always picks the action with largest value.\n\t'

    def act(self, qvals):
        return np.argmax(qvals)


class EpsGreedy(Policy):
    __doc__ = 'Epsilon-Greedy Policy\n\t\n\tThis policy picks the action with largest value with probability 1-epsilon.\n\tIt picks a random action and therefore explores with probability epsilon.\n\t'

    def __init__(self, eps):
        self.eps = eps

    def act(self, qvals):
        if random.random() > self.eps:
            return np.argmax(qvals)
        else:
            return random.randrange(len(qvals))


class GaussianEpsGreedy(Policy):
    __doc__ = 'Gaussian Epsilon-Greedy Policy\n\n\tLike the Epsilon-Greedy Policy except it samples epsilon from a [0,1]-truncated Gaussian distribution.\n\tThis method is used in "Asynchronous Methods for Deep Reinforcement Learning" (Mnih et al., 2016).\n\t'

    def __init__(self, eps_mean, eps_std):
        self.eps_mean = eps_mean
        self.eps_std = eps_std

    def act(self, qvals):
        eps = truncnorm.rvs((0 - self.eps_mean) / self.eps_std, (1 - self.eps_mean) / self.eps_std)
        if random.random() > eps:
            return np.argmax(qvals)
        else:
            return random.randrange(len(qvals))


class PassThrough(Policy):
    __doc__ = "Pass-Through Policy\n\n\tThis policy simply outputs the model's output, unchanged.\n\t"

    def act(self, action):
        return action