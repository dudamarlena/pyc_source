# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/mcts/tree_policies.py
# Compiled at: 2015-03-25 05:48:43
# Size of source mod 2**32: 644 bytes
from __future__ import division
import numpy as np

class UCB1(object):
    __doc__ = '\n    The typical bandit upper confidence bounds algorithm.\n    '

    def __init__(self, c):
        self.c = c

    def __call__(self, action_node):
        if self.c == 0:
            return action_node.q
        return action_node.q + self.c * np.sqrt(2 * np.log(action_node.parent.n) / action_node.n)


def flat(_):
    """
    All actions are considered equally useful
    :param _:
    :return:
    """
    return 0