# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/diff/diff_item.py
# Compiled at: 2018-08-22 07:31:57
# Size of source mod 2**32: 678 bytes
import abc

class DiffItem(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, differ, **kwargs):
        self.differ = differ
        self.kwargs = kwargs

    @abc.abstractmethod
    def deltas(self):
        pass

    @property
    def lhs(self):
        return self.differ.lhs

    @property
    def rhs(self):
        return self.differ.rhs

    def __repr__(self):
        return '{kls} ({d}, {k})'.format(kls=(self.__class__.__name__), d=(self.differ),
          k=(self.kwargs))

    def __str__(self):
        return str(self.__class__.__name__)