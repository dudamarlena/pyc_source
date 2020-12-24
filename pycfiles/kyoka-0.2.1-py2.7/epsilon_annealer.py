# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/callback/epsilon_annealer.py
# Compiled at: 2016-10-28 02:21:50
from kyoka.callback.base_callback import BaseCallback
from kyoka.policy.epsilon_greedy_policy import EpsilonGreedyPolicy

class EpsilonAnnealer(BaseCallback):

    def __init__(self, epsilon_greedy_policy):
        self.policy = epsilon_greedy_policy
        self.anneal_finished = False

    def define_log_tag(self):
        return 'EpsilonGreedyAnnealing'

    def before_gpi_start(self, _domain, _value_function):
        start_msg = 'Anneal epsilon from %s to %s.' % (self.policy.eps, self.policy.min_eps)
        self.log(start_msg)

    def after_update(self, iteration_count, _domain, _value_function):
        self.policy.anneal_eps()
        if not self.anneal_finished and self.policy.eps == self.policy.min_eps:
            self.anneal_finished = True
            finish_msg = 'Annealing has finished at %d iteration.' % iteration_count
            self.log(finish_msg)