# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/algorithm/td_learning/base_td_method.py
# Compiled at: 2016-10-19 02:53:29
from kyoka.algorithm.base_rl_algorithm import BaseRLAlgorithm
from kyoka.value_function.base_action_value_function import BaseActionValueFunction
from kyoka.value_function.base_state_value_function import BaseStateValueFunction

class BaseTDMethod(BaseRLAlgorithm):

    def update_action_value_function(self, domain, policy, value_function):
        err_msg = self.__build_err_msg('update_action_value_function')
        raise NotImplementedError(err_msg)

    def update_value_function(self, domain, policy, value_function):
        self.__reject_state_value_function(value_function)
        self.update_action_value_function(domain, policy, value_function)

    def __reject_state_value_function(self, value_function):
        if not isinstance(value_function, BaseActionValueFunction):
            msg = 'TD method requires you to use "ActionValueFunction" (child class of [ BaseActionValueFunction ])'
            raise TypeError(msg)

    def __build_err_msg(self, msg):
        base_msg = '[ {0} ] class does not implement [ {1} ] method'
        return base_msg.format(self.__class__.__name__, msg)