# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/agent/cem_agent.py
# Compiled at: 2018-03-04 11:41:49
# Size of source mod 2**32: 5867 bytes
"""
    CEM Agent class, which takes in a PolicyModel object

[1] Learning Tetris with the Noisy Cross-Entropy Method
    (Szita, Lorincz 2006)
    pdf: http://nipg.inf.elte.hu/publications/szita06learning.pdf
"""
from yarlp.agent.base_agent import Agent
from yarlp.model.model_factories import cem_model_factory
from yarlp.agent.base_agent import do_rollout
from yarlp.model.networks import mlp
import numpy as np

class CEMAgent(Agent):
    __doc__ = '\n    Cross Entropy Method\n\n    where Z_t = max(alpha - t / beta) from equation (2.5)\n\n    Parameters\n    ----------\n    policy_model : model.Model\n\n    n_weight_samples : integer\n        Total number of sample weights to draw during each training step\n\n    init_var : float, default 0.1\n\n    best_pct : float, default 0.2\n        The percentage of sample weights to keep that yield the best reward\n    '

    def __init__(self, env, n_weight_samples=100, init_var=1.0, best_pct=0.2, policy_network=None, policy_network_params={}, model_file_path=None, min_std=1e-06, init_std=1.0, adaptive_std=False, *args, **kwargs):
        super().__init__(env, *args, **kwargs)
        if policy_network is None:
            policy_network = mlp
        self._policy = cem_model_factory(env, policy_network, policy_network_params, min_std=min_std, init_std=init_std, adaptive_std=adaptive_std, model_file_path=model_file_path)
        self.tf_object_attributes.add('_policy')
        theta = self._policy.G(self._policy['gf'])
        self.model_total_sizes = theta.shape[0]
        self._theta = np.zeros(self.model_total_sizes)
        self._sigma = np.ones(self.model_total_sizes) * init_var
        self.n_weight_samples = n_weight_samples
        assert best_pct <= 1 and best_pct > 0
        self.num_best = int(best_pct * self.n_weight_samples)

    def train(self, num_train_steps=1, num_test_steps=0, max_timesteps=0, n_steps=None, with_variance=False, alpha=5, beta=10, min_sigma=0.01, render=False):
        """
        Learn the most optimal weights for our PolicyModel
            optionally with a variance adjustment as in [1]
            as Z_t = max(alpha - t / beta)

        Parameters
        ----------
        num_training_steps : integer
            Total number of training steps

        max_timesteps : integer
            maximum number of total steps to execute in the environment

        with_variance : boolean
            train with or without a variance adjustment as in [1]

        alpha : float, default 5
            parameter for variance adjustment (Z_t = max(alpha - t / beta))

        beta : float, default 10
            parameter for variance adjustment (Z_t = max(alpha - t / beta))

        render : bool, whether to render episodes in a video

        Returns
        ----------
        None
        """
        assert sum([num_train_steps > 0,
         max_timesteps > 0]) == 1, 'Must provide at least one limit to training'
        timesteps_so_far = 0
        train_steps_so_far = 0
        rollout_gen = do_rollout(self, self._env, n_steps, greedy=False, render=render)
        while True:
            if max_timesteps and timesteps_so_far >= max_timesteps:
                break
            elif num_train_steps and train_steps_so_far >= num_train_steps:
                break
            if np.any(self._sigma <= 0):
                self._sigma[self._sigma <= 0] = min_sigma
            weight_samples = np.array([np.random.normal(mean, np.sqrt(var), self.n_weight_samples) for mean, var in zip(self._theta, self._sigma)])
            weight_samples = weight_samples.T
            rollouts = []
            rollout_rewards = []
            for w in weight_samples:
                self._policy.G(self._policy['sff'], {self._policy['theta']: w})
                rollout = rollout_gen.__next__()
                timesteps_so_far += len(rollout['dones'])
                rollouts.append(rollout)
                rollout_rewards.append(np.sum(rollout['rewards']))

            rollout_rewards = np.array(rollout_rewards)
            self.logger.set_metrics_for_rollout(rollouts, train=True)
            self.logger.log()
            best_idx = rollout_rewards.argsort()[::-1][:self.num_best]
            best_samples = weight_samples[best_idx]
            mean = best_samples.mean(axis=0)
            var = best_samples.var(axis=0)
            if with_variance:
                var += max(alpha - train_steps_so_far / float(beta), 0)
            self._theta = mean
            self._sigma = var
            if num_test_steps > 0:
                r = []
                for t_test in range(num_test_steps):
                    rollout = self.rollout(greedy=True)
                    r.append(rollout)

                self.logger.set_metrics_for_rollout(r, train=False)
                self.logger.log()
            if self.logger._log_dir is not None:
                self.save_models(self.logger._log_dir)
            train_steps_so_far += 1