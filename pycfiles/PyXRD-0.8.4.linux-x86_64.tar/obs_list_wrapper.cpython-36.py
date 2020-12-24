# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/obs_list_wrapper.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2193 bytes
from .obs_seq_wrapper import ObsSeqWrapper
from .value_wrapper import ValueWrapper

@ValueWrapper.register_wrapper(position=0)
class ObsListWrapper(ObsSeqWrapper):

    @classmethod
    def wrap_value(cls, label, value, model=None):
        if isinstance(value, list):
            res = cls(value)
            if model:
                res.__add_model__(model, label)
            return res

    def __init__(self, l):
        methods = ('append', 'extend', 'insert', 'pop', 'remove', 'reverse', 'sort')
        ObsSeqWrapper.__init__(self, l, methods)
        for _m in ('add', 'mul'):
            meth = '__%s__' % _m
            assert hasattr(self._obj, meth), 'Not found method %s in %s' % (meth, str(type(self._obj)))
            setattr(self.__class__, meth, getattr(self._obj, meth))

    def __radd__(self, other):
        return other.__add__(self._obj)

    def __rmul__(self, other):
        return self._obj.__mul__(other)