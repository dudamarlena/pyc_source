# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/utils/exploration_noise.py
# Compiled at: 2018-01-09 00:34:26
# Size of source mod 2**32: 2593 bytes
from __future__ import division
import numpy as np

class ExplorationNoise(object):
    __doc__ = 'Noise that is added to action exploration for deterministic policies.\n    '

    def __init__(self):
        pass

    def sample_noise(self):
        raise NotImplementedError()

    def reset(self):
        pass

    def add_noise_to_action(self, env, action):
        """Adds noise to action clipped with Box action space
        """
        noise = self.sample_noise()
        noisy_action = np.clip(action + noise, env.action_space.low, env.action_space.high)
        return noisy_action


class AnnealedGaussian(ExplorationNoise):
    __doc__ = 'Annealed Gaussian Noise\n    '

    def __init__(self, mu, max_sigma, min_sigma, n_actions=1, n_annealing_steps=1000000):
        super(AnnealedGaussian, self).__init__()
        assert max_sigma > min_sigma
        assert min_sigma > 0
        self._t = 0
        self._mu = mu
        self._max_sigma = max_sigma
        self._min_sigma = min_sigma
        self.n_actions = n_actions
        self.n_annealing_steps = float(n_annealing_steps)

    @property
    def sigma(self):
        annealed_proportion = (self._max_sigma - self._min_sigma) * min(1.0, self._t / self.n_annealing_steps)
        sigma = self._max_sigma - annealed_proportion
        return sigma

    def sample_noise(self):
        self._t += 1
        return np.random.normal(loc=self._mu, scale=self.sigma, size=self.n_actions)


class OrnsteinUhlenbeck(ExplorationNoise):
    __doc__ = 'Ornstein-Uhlenbeck process, time-correlated noise\n    dx_t = theta * (mu - x_t) * dt + sigma dW_t\n    where dW_t is a Weiner process\n    '

    def __init__(self, mu, theta, sigma, n_actions=1, dt=1):
        super(OrnsteinUhlenbeck, self).__init__()
        assert theta > 0
        assert sigma > 0
        assert dt > 0
        self._mu = mu
        self._theta = theta
        self._sigma = sigma
        self._dt = dt
        self.n_actions = n_actions
        self._x = None
        self.reset()

    @property
    def sigma(self):
        return self._sigma

    def sample_noise(self):
        assert self._x is not None
        dx = self._theta * (self._mu - self._x) * self._dt
        dx += self.sigma * np.sqrt(self._dt) * np.random.normal(size=self.n_actions)
        self._x = self._x + dx
        return self._x

    def reset(self):
        self._x = np.ones(self.n_actions) * self._mu


class AnnealedOrnsteinUhlenbeck(AnnealedGaussian):

    def __init__(self):
        raise NotImplementedError()