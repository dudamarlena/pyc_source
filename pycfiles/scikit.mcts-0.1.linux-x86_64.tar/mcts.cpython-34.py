# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/mcts/mcts.py
# Compiled at: 2015-03-25 05:37:45
# Size of source mod 2**32: 1662 bytes
from __future__ import print_function
import random
from . import utils

class MCTS(object):
    __doc__ = '\n    The central MCTS class, which performs the tree search. It gets a\n    tree policy, a default policy, and a backup strategy.\n    See e.g. Browne et al. (2012) for a survey on monte carlo tree search\n    '

    def __init__(self, tree_policy, default_policy, backup):
        self.tree_policy = tree_policy
        self.default_policy = default_policy
        self.backup = backup

    def __call__(self, root, n=1500):
        """
        Run the monte carlo tree search.

        :param root: The StateNode
        :param n: The number of roll-outs to be performed
        :return:
        """
        if root.parent is not None:
            raise ValueError("Root's parent must be None.")
        for _ in range(n):
            node = _get_next_node(root, self.tree_policy)
            node.reward = self.default_policy(node)
            self.backup(node)

        return utils.rand_max(root.children.values(), key=lambda x: x.q).action


def _expand(state_node):
    action = random.choice(state_node.untried_actions)
    return state_node.children[action].sample_state()


def _best_child(state_node, tree_policy):
    best_action_node = utils.rand_max(state_node.children.values(), key=tree_policy)
    return best_action_node.sample_state()


def _get_next_node(state_node, tree_policy):
    while not state_node.state.is_terminal():
        if state_node.untried_actions:
            return _expand(state_node)
        state_node = _best_child(state_node, tree_policy)

    return state_node