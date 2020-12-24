# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/utils.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 875 bytes
"""
Miscellaneous utilities used throughout the library.
"""
import collections.abc

class IterToAiter(collections.abc.Iterator, collections.abc.AsyncIterator):
    __doc__ = '\n    Transforms an `__iter__` method into an `__aiter__` method.\n    '

    def __init__(self, iterator: collections.abc.Iterator):
        self._it = iterator

    def __iter__(self):
        return self

    def __next__(self):
        return self._it.__next__()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return self.__next__()
        except StopIteration:
            raise StopAsyncIteration


def iter_to_aiter(type_):
    """
    Transforms a normal iterable type into an async iterable type.
    """

    def __aiter__(self):
        return IterToAiter(iter(self))

    type_.__aiter__ = __aiter__
    return type_