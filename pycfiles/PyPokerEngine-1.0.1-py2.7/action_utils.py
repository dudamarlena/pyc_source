# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/utils/action_utils.py
# Compiled at: 2017-04-01 23:56:44
from pypokerengine.engine.action_checker import ActionChecker
ACTION_CALL = 'call'
ACTION_FOLD = 'fold'
ACTION_RAISE = 'raise'

def generate_legal_actions(players, player_position, sb_amount):
    return ActionChecker.legal_actions(players, player_position, sb_amount)


def is_legal_action(players, player_position, sb_amount, action, amount=None):
    return ActionChecker._is_legal(players, player_position, sb_amount, action, amount)