# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sample/ticktacktoe/ticktacktoe_manual_policy.py
# Compiled at: 2016-09-21 07:18:42
from kyoka.policy.base_policy import BasePolicy

class TickTackToeManualPolicy(BasePolicy):
    ACTION_NAME_MAP = {1: 'lower_right', 
       2: 'lower_center', 
       4: 'lower_left', 
       8: 'middle_right', 
       16: 'middle_center', 
       32: 'middle_left', 
       64: 'upper_right', 
       128: 'upper_center', 
       256: 'upper_left'}

    def choose_action(self, state):
        message = self.__ask_message(state) + ' >> '
        action = int(raw_input(message))
        if action not in self.domain.generate_possible_actions(state):
            return self.choose_action(state)
        return action

    def __ask_message(self, state):
        possible_actions = self.domain.generate_possible_actions(state)
        names = [ self.ACTION_NAME_MAP[action] for action in possible_actions ]
        return (', ').join([ '%d: %s' % info for info in zip(possible_actions, names) ])