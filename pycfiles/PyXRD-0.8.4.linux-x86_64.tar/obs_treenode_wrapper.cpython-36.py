# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/obs_treenode_wrapper.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1821 bytes
from .obs_wrapper import ObsWrapper
from .value_wrapper import ValueWrapper

@ValueWrapper.register_wrapper(position=2)
class ObsTreeNodeWrapper(ObsWrapper):

    @classmethod
    def wrap_value(cls, label, value, model=None):
        from ...models.treenode import TreeNode
        if isinstance(value, TreeNode):
            res = cls(value)
            if model:
                res.__add_model__(model, label)
            return res

    def __init__(self, t):
        methods = ('insert', 'remove', 'on_grandchild_inserted', 'on_grandchild_removed')
        ObsWrapper.__init__(self, t, methods)