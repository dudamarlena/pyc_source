# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/obs_seq_wrapper.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2397 bytes
from .obs_wrapper import ObsWrapper

class ObsSeqWrapper(ObsWrapper):
    __doc__ = '\n        Base class for ObsListWrapper, ObsMapWrapper, ...\n        Use sub-classes, not this base class!\n    '

    def __init__(self, obj, method_names):
        ObsWrapper.__init__(self, obj, method_names)
        for _m in 'lt le eq ne gt ge len iter'.split():
            meth = '__%s__' % _m
            assert hasattr(self._obj, meth), 'Not found method %s in %s' % (meth, str(type(self._obj)))
            setattr(self.__class__, meth, getattr(self._obj, meth))

    def __setitem__(self, key, val):
        self._notify_method_before(self._obj, '__setitem__', (key, val), {})
        res = self._obj.__setitem__(key, val)
        self._notify_method_after(self._obj, '__setitem__', res, (key, val), {})
        return res

    def __delitem__(self, key):
        self._notify_method_before(self._obj, '__delitem__', (key,), {})
        res = self._obj.__delitem__(key)
        self._notify_method_after(self._obj, '__delitem__', res, (key,), {})
        return res

    def __getitem__(self, key):
        return self._obj.__getitem__(key)