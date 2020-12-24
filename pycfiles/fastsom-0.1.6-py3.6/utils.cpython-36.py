# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/core/utils.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 3690 bytes
"""
This file contains various project-wide utilities.

"""
from typing import Collection, Callable
from functools import reduce
__all__ = [
 'ifnone',
 'ifindict',
 'is_iterable',
 'listify',
 'setify',
 'compose',
 'enum_eq']

def ifnone(o: any, default: any) -> any:
    """
    Returns `o` if it is not `None`; returns `default` otherwise.

    Parameters
    ----------
    o : any
        The value to be checked.
    default : any
        The default return value when `o` is `None`.

    Examples
    --------
    >>> ifnone(5, 'default-value')
    5

    >>> ifnone(None, 42)
    42
    """
    if o is not None:
        return o
    else:
        return default


def ifindict(d: dict, k: str, default: any) -> any:
    """
    Returns the value of `k` inside `d` if it exists; returns `default` otherwise.

    Parameters
    ----------
    d : dict
        The source dict.
    k : str
        The lookup key
    default : any
        The default return value when `k` is not in `d`.

    Examples
    --------
    >>> d = dict(a=5, b=6)
    >>> ifindict(d, 'a', 'default-value')
    5
    >>> ifindict(d, 'some_invalid_key', 42)
    42
    """
    if k in d:
        return d[k]
    else:
        return default


def is_iterable(o: any) -> bool:
    """
    Checks if `o` is iterable

    Parameters
    ----------
    o : any
        The value to be checked.

    Examples
    --------
    >>> is_iterable(list(range(5)))
    True

    >>> is_iterable(5)
    False

    >>> is_iterable('hello world')
    True

    >>> is_iterable(None)
    False
    """
    try:
        _ = iter(o)
    except TypeError:
        return False
    else:
        return True


def listify(o: any) -> list:
    """
    Turns `o` into a list.

    Parameters
    ----------
    o : any
        The value to be listified.

    Examples
    --------
    >>> listify(None)
    []

    >>> listify('mystring')
    ['m', 'y', 's', 't', 'r', 'i', 'n', 'g']

    >>> listify(5)
    5
    """
    if o is None:
        return []
    else:
        if not is_iterable(o):
            return o
        if isinstance(o, list):
            return o
        return list(o)


def setify(o: any) -> set:
    """
    Turns `o` into a set.

    Parameters
    ----------
    o : any
        The value to be setified.

    Examples
    --------
    >>> setify(5)
    5

    >>> setify(None)
    set()

    >>> setify('hello world')
    {'h', 'l', 'd', 'e', 'w', 'r', ' ', 'o'}

    >>> setify([1, 2, 2, 3, 3, 4, 5])
    {1, 2, 3, 4, 5}
    """
    if o is None:
        return set()
    else:
        if not is_iterable(o):
            return o
        if isinstance(o, set):
            return o
        return set(listify(o))


def compose(x: any, fns: Collection[Callable], order_key: str='_order', **kwargs) -> any:
    """
    Applies each function in `fns` to the output of the previous function.

    Function application starts from `x`, and uses `order_key` to sort the `fns` list.

    Parameters
    ----------
    x : any
        The base function parameter.
    fns : Collection[Callable]
        The collection of functions.
    order_key : str default='_order'
        The key to be used to sort the functions.
    """
    sorted_fns = sorted((listify(fns)), key=(lambda o: getattr(o, order_key, 0)))
    return reduce(lambda x, fn: fn(x), sorted_fns, x)


def enum_eq(enum, value) -> bool:
    """
    Checks equality of `enum` and `value`.

    Parameters
    ----------
    enum : Enum
        The enumerator instance
    value : any
        The value or enumerator instance to be compared.
    """
    return enum == value or enum.value == value