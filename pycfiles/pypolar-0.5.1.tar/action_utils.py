# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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