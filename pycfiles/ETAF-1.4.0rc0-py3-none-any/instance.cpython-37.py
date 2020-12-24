# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/feature/instance.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1584 bytes


class Instance(object):
    __doc__ = '\n    Instance object use in all algorithm module\n\n    Parameters\n    ----------\n    inst_id : int, the id of the instance, reserved fields in this version\n\n    weight: float, the weight of the instance\n\n    feature : object, ndarray or SparseVector Object in this version\n\n    label: None of float, data label\n\n    '

    def __init__(self, inst_id=None, weight=1.0, features=None, label=None):
        self.inst_id = inst_id
        self.weight = weight
        self.features = features
        self.label = label

    def set_weight(self, weight=1.0):
        self.weight = weight

    def set_label(self, label=1):
        self.label = label

    def set_feature(self, features):
        self.features = features