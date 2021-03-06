# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/agent/pg_agents.py
# Compiled at: 2018-03-04 11:41:49
# Size of source mod 2**32: 2882 bytes
"""
REINFORCE Agent and Policy Gradient (PG) Actor Critic Agent

[1] Simple statistical gradient-following algorithms for connectionist
    reinforcement learning (Williams, 1992)
    pdf: http://link.springer.com/article/10.1007/BF00992696

[2] Sutton, R. S., Mcallester, D., Singh, S., & Mansour, Y. (1999).
    Policy Gradient Methods for Reinforcement Learning with
    Function Approximation. Advances in Neural Information Processing
    Systems 12, 1057–1063. doi:10.1.1.37.9714

[3] Degris, T., Pilarski, P., & Sutton, R. (2012). Model-free reinforcement
    learning with continuous action in practice. … Control Conference (ACC),
    2177–2182. doi:10.1109/ACC.2012.6315022
"""
import numpy as np
from yarlp.agent.base_agent import BatchAgent
from yarlp.model.model_factories import pg_model_factory
from yarlp.utils.experiment_utils import get_network
from yarlp.model.networks import mlp

class REINFORCEAgent(BatchAgent):
    __doc__ = '\n    REINFORCE - Monte Carlo Policy Gradient for discrete action spaces\n\n    Parameters\n    ----------\n    env : gym.env\n\n    policy_network : model.Model\n\n    baseline_network : if None, we us no baseline\n        otherwise we use a LinearFeatureBaseline as default\n        you can also pass in a function as a tensorflow network which\n        gets built by the value_function_model_factory\n\n    entropy_weight : float, coefficient on entropy in the policy gradient loss\n\n    model_file_path : str, file path for the policy_network\n    '

    def __init__(self, env, policy_network=None, policy_network_params={}, policy_learning_rate=0.01, entropy_weight=0, model_file_path=None, adaptive_std=False, init_std=1.0, min_std=1e-06, gae_lambda=1.0, *args, **kwargs):
        super().__init__(env, *args, **kwargs)
        if policy_network is None:
            policy_network = mlp
        policy_network = get_network(policy_network, policy_network_params)
        self._policy = pg_model_factory(env, network=policy_network, network_params=policy_network_params, learning_rate=policy_learning_rate, entropy_weight=entropy_weight, min_std=min_std, init_std=init_std, adaptive_std=adaptive_std, model_file_path=model_file_path)
        self.tf_object_attributes.add('_policy')
        policy_weight_sums = sum([np.sum(a) for a in self._policy.get_weights()])
        self.logger.logger.info('Policy network weight sums: {}'.format(policy_weight_sums))
        self._gae_lambda = gae_lambda

    def update(self, path):
        loss = self._policy.update(path['observations'], path['advantages'], path['actions'])
        self.logger.add_metric('policy_loss', loss)