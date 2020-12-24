# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/patch/patch_item.py
# Compiled at: 2018-08-26 08:41:53
# Size of source mod 2**32: 748 bytes
import abc
from diff_and_patch.delta import Delta

class PatchItem(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, patcher, delta, **kwargs):
        self.patcher = patcher
        assert isinstance(delta, Delta)
        self.delta = delta
        self.kwargs = kwargs

    @classmethod
    @abc.abstractmethod
    def diff_class(cls):
        pass

    @abc.abstractmethod
    def apply(self):
        pass

    def __repr__(self):
        return '{p}: {c} -> {n}'.format(p=(self.__class__.__name__), c=(self.delta.current_state),
          n=(self.delta.new_state))

    def __str__(self):
        return self.__repr__()