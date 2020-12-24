# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/_utils.py
# Compiled at: 2015-07-31 13:31:44
"""
Tools for storage implementations.

Your use of this software is governed by your license agreement.

Copyright 2012-2015 Diffeo, Inc.
"""
import uuid, itertools
from kvlayer._exceptions import StorageClosed, BadKey, SerializationError

def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    args = [
     iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def _requires_connection(func):
    """
    Decorator for methods on any implementation of AbstractStorage.
    Raises StorageClosed when self._connected is not True.
    """

    def wrapped_func(self, *args, **kwargs):
        if not self._connected:
            raise StorageClosed()
        return func(self, *args, **kwargs)

    return wrapped_func


def split_uuids(uuid_str):
    """
    DEPRECATED. Only used in Cassandra backend.
    """
    if '\x00' in uuid_str:
        return uuid_str.split('\x00')
    return map(lambda s: uuid.UUID(hex=('').join(s)), grouper(uuid_str, 32))


def join_uuids(*uuids):
    """
    DEPRECATED. Only used in Cassandra backend.
    """
    if not uuids or uuids[0] == '':
        uuid_str = ''
    else:
        uuid_str = ('').join(map(lambda x: x.hex, uuids))
    return uuid_str


class batches(object):
    """
    return lists of length n drawn from an iterable.  The last batch
    may be shorter than n.
    """

    def __init__(self, iterable, n):
        self.items = iter(iterable)
        self.n = n

    def __iter__(self):
        batch = []
        for i in self.items:
            batch.append(i)
            if len(batch) == self.n:
                yield batch
                batch = []

        if batch:
            yield batch