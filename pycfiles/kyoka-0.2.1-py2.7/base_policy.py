# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/policy/base_policy.py
# Compiled at: 2016-10-26 09:22:48
from kyoka.value_function.base_action_value_function import BaseActionValueFunction
from kyoka.value_function.base_state_value_function import BaseStateValueFunction

class BasePolicy(object):

    def choose_action(self, domain, value_function, state, action=None):
        err_msg = self.__build_err_msg('choose_action')
        raise NotImplementedError(err_msg)

    def pack_arguments_for_value_function(self, value_function, state, action):
        if isinstance(value_function, BaseStateValueFunction):
            return [state]
        if isinstance(value_function, BaseActionValueFunction):
            return [state, action]
        raise ValueError('Invalid value function is set')

    def __build_err_msg(self, msg):
        base_msg = '[ {0} ] class does not implement [ {1} ] method'
        return base_msg.format(self.__class__.__name__, msg)