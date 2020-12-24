# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/policy/greedy_policy.py
# Compiled at: 2016-10-26 09:22:48
import random
from kyoka.policy.base_policy import BasePolicy

class GreedyPolicy(BasePolicy):

    def __init__(self, rand=None):
        self.rand = rand if rand else random

    def choose_action(self, domain, value_function, state):
        actions = domain.generate_possible_actions(state)
        pack = lambda state, action: self.pack_arguments_for_value_function(value_function, state, action)
        calc_Q_value = lambda packed_arg: value_function.calculate_value(*packed_arg)
        Q_value_for_actions = [ calc_Q_value(pack(state, action)) for action in actions ]
        max_Q_value = max(Q_value_for_actions)
        Q_act_pair = zip(Q_value_for_actions, actions)
        best_actions = [ act for Q_value, act in Q_act_pair if max_Q_value == Q_value ]
        best_action = self.rand.choice(best_actions)
        return best_action