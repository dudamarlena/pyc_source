# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/coding/structures/typednamedtuple.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 1595 bytes
import typing as tp
from collections import namedtuple
__all__ = [
 'typednamedtuple']

def _nth(it, n):
    return [x[n] for x in it]


def _adjust(q):
    var, type_ = q
    if type_ in (None, 'self') or isinstance(var, type_):
        return var
    return type_(var)


def typednamedtuple(cls_name: str, *arg_name_type: type) -> tp.Type[tp.Tuple]:
    """
    Returns a new subclass of tuple with named fields.
    Fields will be coerced to type passed in the pair.

    Parameters are tuples of (field name, class/constructor as callable/1)

    For example:

    >>> tnt = typednamedtuple('tnt', ('x', float), ('y', float))
    >>> a = tnt('5.0', y=2)

    a.x is float, a.y is float too
    """
    fieldnames = []
    typeops = []
    mapping = {}
    for name, type_ in arg_name_type:
        fieldnames.append(name)
        typeops.append(type_)
        mapping[name] = type_

    MyCls = namedtuple(cls_name, fieldnames)

    class Wrapper(MyCls):
        __doc__ = MyCls.__doc__
        __name__ = MyCls.__name__

        def __new__(cls, *args, **kwargs):
            nargs = list(map(_adjust, zip(args, typeops[:len(args)])))
            for next_field_name in fieldnames[len(nargs):]:
                try:
                    nargs.append(_adjust((kwargs.pop(next_field_name), mapping[next_field_name])))
                except KeyError:
                    raise TypeError('Field %s not given', next_field_name)

            if len(kwargs) > 0:
                raise TypeError('Too many parameters')
            return (MyCls.__new__)(MyCls, *nargs)

    return Wrapper