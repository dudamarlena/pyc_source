# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/immutable.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 1638 bytes
from abc import ABCMeta
__all__ = ['Immutable', 'frozendict']

class ImmutableMetaType(ABCMeta):

    def __call__(cls, *args, **kwargs):
        p = (type.__call__)(cls, *args, **kwargs)
        p.__dict__['_Immutable__locked_for_writes'] = True
        return p


class Immutable(metaclass=ImmutableMetaType):
    __doc__ = "\n    A mix-in to make your classes immutable.\n\n    You can assign normally using your constructor.\n\n    >>> class Test(Immutable):\n    >>>     def __init__(self):\n    >>>         self.attribute = 'value'\n    "
    _Immutable__locked_for_writes = False

    def __setattr__(self, attr, value):
        if self._Immutable__locked_for_writes:
            raise TypeError('%s does not support attribute assignment' % (self.__class__.__qualname__,))
        else:
            super().__setattr__(attr, value)

    def __delattr__(self, attr):
        if self._Immutable__locked_for_writes:
            raise TypeError('%s does not support attribute deletion' % (self.__class__.__qualname__,))
        else:
            super().__delattr__(attr)


class frozendict(dict):
    __doc__ = "\n    A hashable dict with express forbid to change it's values\n    Both keys and values must be hashable in order for this dict to be hashable.\n    "

    def __setitem__(self, key, value):
        raise TypeError('Cannot update a frozen dict!')

    def update(self, *args, **kwargs):
        raise TypeError('Cannot update a frozen dict!')

    def __hash__(self):
        o = 0
        for key, value in self.items():
            o = o ^ hash(key) ^ hash(value)

        return o