# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/mcts/backups.py
# Compiled at: 2015-03-25 05:42:29
# Size of source mod 2**32: 1222 bytes
from __future__ import division
from .graph import StateNode, ActionNode

class Bellman(object):
    __doc__ = '\n    A dynamical programming update which resembles the Bellman equation\n    of value iteration.\n\n    See Feldman and Domshlak (2014) for reference.\n    '

    def __init__(self, gamma):
        self.gamma = gamma

    def __call__(self, node):
        """
        :param node: The node to start the backups from
        """
        while node is not None:
            node.n += 1
            if isinstance(node, StateNode):
                node.q = max([x.q for x in node.children.values()])
            elif isinstance(node, ActionNode):
                n = sum([x.n for x in node.children.values()])
                node.q = sum([(self.gamma * x.q + x.reward) * x.n for x in node.children.values()]) / n
            node = node.parent


def monte_carlo(node):
    """
    A monte carlo update as in classical UCT.

    See feldman amd Domshlak (2014) for reference.
    :param node: The node to start the backup from
    """
    r = node.reward
    while node is not None:
        node.n += 1
        node.q = (node.n - 1) / node.n * node.q + 1 / node.n * r
        node = node.parent