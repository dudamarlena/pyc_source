# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/coding/sequences/choose.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 884 bytes
import typing as tp
T = tp.TypeVar('T')
__all__ = [
 'choose']

def choose(filter_fun: tp.Callable[([T], bool)], iterable: tp.Iterable[T]) -> T:
    """
    Return a single value that exists in given iterable

    :param filter_fun: function that returns bool on the single value
    :param iterable: iterable to examine
    :return: single element in the iterable that matches given input
    :raises ValueError: on multiple elements matching, or none at all
    """
    elem_candidate = None
    found = False
    for elem in iterable:
        if filter_fun(elem):
            if found:
                raise ValueError('Multiple values (%s, %s) seen' % (repr(elem_candidate), repr(elem)))
            elem_candidate = elem
            found = True

    if not found:
        raise ValueError('No elements matching given filter seen')
    return elem_candidate