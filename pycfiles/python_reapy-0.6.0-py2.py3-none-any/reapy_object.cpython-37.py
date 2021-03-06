# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\core\reapy_object.py
# Compiled at: 2020-03-21 05:50:19
# Size of source mod 2**32: 1615 bytes
import reapy

class ReapyMetaclass(type):

    @property
    def _reapy_parent(self):
        """Return first reapy parent class."""
        for candidate in self.__mro__:
            if candidate.__module__.startswith('reapy.'):
                return candidate


class ReapyObject(metaclass=ReapyMetaclass):
    __doc__ = 'Base class for reapy objects.'

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):

        def to_str(x):
            if isinstance(x, str):
                return '"{}"'.format(x)
            return str(x)

        args = ', '.join(map(to_str, self._args))
        kwargs = ', '.join(('{}={}'.format(k, to_str(v)) for k, v in self._kwargs.items()))
        if args and kwargs:
            brackets = ', '.join((args, kwargs))
        else:
            brackets = args if args else kwargs
        rep = '{}({})'.format(self.__class__.__name__, brackets)
        return rep

    @property
    def _args(self):
        return ()

    @property
    def _is_defined(self):
        if hasattr(self, 'id'):
            return not self.id.endswith('0x0000000000000000')
        raise NotImplementedError

    @property
    def _kwargs(self):
        return {}

    def _to_dict(self):
        return {'__reapy__':True, 
         'class':self.__class__._reapy_parent.__name__, 
         'args':self._args, 
         'kwargs':self._kwargs}


class ReapyObjectList(ReapyObject):
    __doc__ = 'Abstract class for list of ReapyObjects.'