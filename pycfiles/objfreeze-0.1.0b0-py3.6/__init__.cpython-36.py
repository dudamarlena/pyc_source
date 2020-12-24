# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/objfreeze/__init__.py
# Compiled at: 2018-11-26 23:46:49
# Size of source mod 2**32: 5287 bytes
"""Module provides function to convert data into freezed (immutable) version.
"""
__all__ = ('Error', 'FrozenDict', 'freeze', '__version__')
__version__ = '0.1.0b'

class Error(Exception):
    __doc__ = 'Error helps to catch cases when input data is not immutable.\n\t'


class FrozenDict(dict):
    __doc__ = 'A dict which forbids changes.\n\n\tValues of type list/dict are copied recursively into FrozenDicts/tuples.\n\tGenerators are not allowed as an input value\n\t(i.e. `FrozenDict(k:1 for k in range(10))`.\n\t'

    def __init__(self, *args, **kwargs):
        is_initted = False
        self._hash = None
        ids = {}
        if args:
            if len(args) > 1:
                raise TypeError('%s expected at most 1 arguments, got %i' % (
                 self.__class__.__name__, len(args)))
            arg = args[0]
            if isinstance(arg, dict):
                subdict = _get_dict_for_frozen(arg.items(), ids)
                is_initted = True
                super().__init__(subdict)
            else:
                raise Error('unsupported input: expected dict/%s, got %r' % (
                 type(self).__name__, type(arg).__name__))
            if kwargs:
                subdict = _get_dict_for_frozen(kwargs.items(), ids)
                is_initted or super().__init__(subdict)
        else:
            super().update(subdict)

    def __hash__(self):
        _hash = self._hash
        if _hash is None:
            self._hash = _hash = hash(tuple(sorted(self.items())))
        return _hash

    def __setitem__(self, *args, **kwargs):
        raise TypeError('%r object does not support item assignment' % self.__class__.__name__)

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """The same as `dict.fromkeys`.
                """
        keys = list(iterable)
        vals = [value] * len(keys)
        return cls(dict(zip(keys, vals)))

    def clear(self, *args, **kwargs):
        raise TypeError('%r does not support changes of its items or itself' % self.__class__.__name__)

    pop = clear
    popitem = clear
    update = clear
    setdefault = clear
    __delitem__ = clear


def _chk_cycle(val, ids):
    """Returns tuple (is_new, elem_id, frozen_value) or raises exception.

        It must be used only for mutable types.
        """
    id_val = id(val)
    if id_val not in ids:
        ids[id_val] = None
        return (True, id_val, None)
    frozen_val = ids[id_val]
    if frozen_val is not None:
        return (False, id_val, frozen_val)
    raise Error('Cycle detected')


def _get_dict_for_frozen(pairs, ids):
    ret = {}
    for key, val in pairs:
        try:
            func = _CONVERT_FUNCS[val.__class__]
        except KeyError:
            raise Error('non-copyable object of type %r' % (
             val.__class__.__qualname__,))

        ret[key] = func(val, ids)

    return ret


def _get_frozen_dict(value, ids):
    is_new, elem_id, frozen_value = _chk_cycle(value, ids)
    if not is_new:
        return frozen_value
    else:
        ret = _get_dict_for_frozen(value.items(), ids)
        ret = FrozenDict(ret)
        ids[elem_id] = ret
        return ret


def _get_frozen_list(value, ids):
    is_new, elem_id, frozen_value = _chk_cycle(value, ids)
    if not is_new:
        return frozen_value
    else:
        try:
            ret = tuple(value)
            hash(ret)
            ids[elem_id] = ret
            return ret
        except TypeError:
            pass

        for elem in value:
            if elem.__class__ not in _CONVERT_FUNCS:
                raise Error('non-copyable object of type %r' % (
                 elem.__class__.__qualname__,))

        ret = tuple(_CONVERT_FUNCS[elem.__class__](elem, ids) for elem in value)
        ids[elem_id] = ret
        return ret


def _get_frozen_set(value, ids):
    is_new, elem_id, frozen_value = _chk_cycle(value, ids)
    if is_new:
        frozen_value = frozenset(value)
        ids[elem_id] = frozen_value
    return frozen_value


def _get_frozen_immutable(value, _):
    return value


_CONVERT_FUNCS = {int: _get_frozen_immutable, 
 float: _get_frozen_immutable, 
 str: _get_frozen_immutable, 
 bytes: _get_frozen_immutable, 
 frozenset: _get_frozen_immutable, 
 type(None): _get_frozen_immutable, 
 FrozenDict: _get_frozen_immutable, 
 set: _get_frozen_set, 
 dict: _get_frozen_dict, 
 list: _get_frozen_list, 
 tuple: _get_frozen_list}

def freeze(value):
    """Return freeze version of value.

        It will be converted if necessary, otherwise returned itself.
        """
    ids = {}
    if value.__class__ not in _CONVERT_FUNCS:
        raise Error('non-copyable object of type %r' % (
         value.__class__.__qualname__,))
    return _CONVERT_FUNCS[value.__class__](value, ids)