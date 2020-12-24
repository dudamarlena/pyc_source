# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/lsqfitgp/_Deriv.py
# Compiled at: 2020-04-22 07:26:33
# Size of source mod 2**32: 2856 bytes
import collections, numpy as np
__all__ = [
 'Deriv']

class Deriv:
    __doc__ = '\n    Class for specifying derivatives. Behaves like a dictionary str -> int,\n    where the keys represent variables and values the derivation order. An\n    empty Deriv means no derivatives. A Deriv with one single key None means\n    that the variable is implicit.\n    '

    def __new__(cls, *args):
        c = collections.Counter()
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Deriv):
                return arg
                if isinstance(arg, (int, np.integer)):
                    assert arg >= 0
                    if arg:
                        c.update({None: arg})
            elif isinstance(arg, str):
                c.update([arg])
            else:
                if np.iterable(arg):
                    integer = None
                    for obj in arg:
                        if isinstance(obj, str):
                            if integer is not None:
                                if integer:
                                    c.update({obj: integer})
                                integer = None
                            else:
                                c.update([obj])
                        elif isinstance(obj, (int, np.integer)):
                            assert obj >= 0
                            integer = int(obj)
                        else:
                            raise TypeError('objects in iterable must be int or str')

                    if integer:
                        raise ValueError('dangling derivative order')
                else:
                    raise TypeError('argument must be int, str, or iterable')
        else:
            if len(args) != 0:
                raise ValueError(len(args))
            assert all(c.values())
            self = super().__new__(cls)
            self._counter = c
            return self

    def __getitem__(self, key):
        return self._counter[key]

    def __iter__(self):
        return iter(self._counter)

    def __bool__(self):
        return bool(self._counter)

    def __eq__(self, val):
        if isinstance(val, Deriv):
            return self._counter == val._counter
        return NotImplemented

    @property
    def implicit(self):
        """
        True if the derivative is trivial or the variable is implicit.
        """
        return not self or next(iter(self._counter)) is None

    @property
    def order(self):
        return sum(self._counter.values())