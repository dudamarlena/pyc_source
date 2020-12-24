# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/utils.py
# Compiled at: 2016-12-01 23:40:36
from __future__ import absolute_import
import os
from kyoka.policy import BasePolicy

def generate_tmp_dir_path(script_path):
    return os.path.join(os.path.dirname(script_path), 'tmp')


def setup_tmp_dir(script_path):
    os.mkdir(generate_tmp_dir_path(script_path))


def teardown_tmp_dir(script_path, file_names):
    dir_path = generate_tmp_dir_path(script_path)
    remove_leaf_dir(dir_path, file_names)


def remove_leaf_dir(dir_path, file_names):
    if os.path.exists(dir_path):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

        os.rmdir(dir_path)


class NegativePolicy(BasePolicy):

    def choose_action(self, task, value_function, state):
        actions = task.generate_possible_actions(state)
        Q_value_for_actions = [ value_function.predict_value(state, action) for action in actions ]
        min_Q_value = min(Q_value_for_actions)
        Q_act_pair = zip(Q_value_for_actions, actions)
        worst_actions = [ act for Q_value, act in Q_act_pair if min_Q_value == Q_value ]
        return worst_actions[0]