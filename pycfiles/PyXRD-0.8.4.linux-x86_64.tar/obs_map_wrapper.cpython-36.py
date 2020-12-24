# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/obs_map_wrapper.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1792 bytes
from .obs_seq_wrapper import ObsSeqWrapper
from .value_wrapper import ValueWrapper

@ValueWrapper.register_wrapper(position=1)
class ObsMapWrapper(ObsSeqWrapper):

    @classmethod
    def wrap_value(cls, label, value, model=None):
        if isinstance(value, dict):
            res = cls(value)
            if model:
                res.__add_model__(model, label)
            return res

    def __init__(self, m):
        methods = ('clear', 'pop', 'popitem', 'update', 'setdefault')
        ObsSeqWrapper.__init__(self, m, methods)