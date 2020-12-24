# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/list.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 5808 bytes
__doc__ = 'PyAMS_utils list module\n\nThis module is dedicated to lists and iterators management. It provides function to extract\nunique values from a list or iterator in their original order, or to iterate over an iterator in\nrandom order; it also provides a "boolean_iter" function (usable as TALES extension) to check if\nan iterator returns at least one value, without consuming this iterator (the function returns a\ntuple containing a boolean value to specify if iterator is empty or not, and the original\niterator).\n'
from itertools import filterfalse, tee
from random import random, shuffle
from zope.interface import Interface
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

def unique(seq, key=None):
    """Extract unique values from list, preserving order

    :param iterator seq: input list
    :param callable key: an identity function which is used to get 'identity' value of each element
        in the list
    :return: list; a new list containing only unique elements of the original list in their initial
        order. Original list is not modified.

    >>> from pyams_utils.list import unique
    >>> mylist = [1, 2, 3, 2, 1]
    >>> unique(mylist)
    [1, 2, 3]

    >>> mylist = [3, 2, 2, 1, 4, 2]
    >>> unique(mylist)
    [3, 2, 1, 4]

    You can also set an 'id' function applied on each element:

    >>> mylist = [1, 2, 3, '2', 4]
    >>> unique(mylist, key=str)
    [1, 2, 3, 4]
    >>> mylist = ['A', 'B', 'b', '2', 4]
    >>> unique(mylist, key=lambda x: str(x).lower())
    ['A', 'B', '2', 4]
    """
    seen = set()
    seen_add = seen.add
    result = []
    if key is None:
        for element in filterfalse(seen.__contains__, seq):
            seen_add(element)
            result.append(element)

    else:
        for element in seq:
            k = key(element)
            if k not in seen:
                seen_add(k)
                result.append(element)

    return result


def unique_iter(iterable, key=None):
    """Iterate over iterator values, yielding only unique values

    :param iterator iterable: input iterator
    :param callable key: an identity function which is used to get 'identity' value of each element
        in the list
    :return: an iterator of unique values

    >>> from pyams_utils.list import unique_iter
    >>> mylist = [1, 2, 3, 2, 1]
    >>> list(unique_iter(mylist))
    [1, 2, 3]

    >>> mylist = [3, 2, 2, 1, 4, 2]
    >>> list(unique_iter(mylist))
    [3, 2, 1, 4]

    You can also set an 'id' function applied on each element:

    >>> mylist = [1, 2, 3, '2', 4]
    >>> list(unique_iter(mylist, key=str))
    [1, 2, 3, 4]
    >>> mylist = ['A', 'B', 'b', '2', 4]
    >>> list(unique_iter(mylist, key=lambda x: str(x).lower()))
    ['A', 'B', '2', 4]
    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element

    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def random_iter(iterable, limit=1):
    """Get items randomly from an iterator

    >>> from pyams_utils.list import random_iter
    >>> mylist = [1, 2, 3, 2, 1]
    >>> list(random_iter(mylist, 2))
    [..., ...]
    """
    selected = [
     None] * limit
    for index, item in enumerate(iterable):
        if index < limit:
            selected[index] = item
        else:
            selected_index = int(random() * (index + 1))
            if selected_index < limit:
                selected[selected_index] = item

    shuffle(selected)
    return iter(selected)


def boolean_iter(iterable):
    """Check if an iterable returns at least one value, without consuming it.

    The function returns a tuple containing a boolean flag indicating if the original iterator
    is empty or not, and the original un-consumed iterator.

    >>> from pyams_utils.list import boolean_iter
    >>> def empty(input):
    ...     yield from input
    >>> mylist = empty(())
    >>> check, myiter = boolean_iter(mylist)
    >>> check
    False
    >>> list(myiter)
    []
    >>> mylist = empty((1,2,3))
    >>> check, myiter = boolean_iter(mylist)
    >>> check
    True
    >>> list(myiter)
    [1, 2, 3]
    >>> list(myiter)
    []
    """

    def inner_check():
        check, items = tee(iterable)
        try:
            next(check)
        except StopIteration:
            yield False
        else:
            yield True
            yield from items

    values = inner_check()
    return (
     next(values), values)


@adapter_config(name='boolean_iter', context=(Interface, Interface, Interface), provides=ITALESExtension)
class IterValuesCheckerExpression(ContextRequestViewAdapter):
    """IterValuesCheckerExpression"""

    def render(self, context=None):
        """Render TALES extension; see `ITALESExtension` interface"""
        if context is None:
            context = self.context
        return boolean_iter(context)