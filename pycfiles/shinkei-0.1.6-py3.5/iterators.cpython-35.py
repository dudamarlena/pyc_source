# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/iterators.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 1077 bytes
import abc
from .exceptions import NoMoreItems

class AbstractAsyncIterator(metaclass=abc.ABCMeta):

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            item = await self.next()
        except NoMoreItems:
            raise StopAsyncIteration()
        else:
            return item

    @abc.abstractmethod
    async def next(self):
        raise NotImplementedError('Must be implemented by subclasses.')


class StreamAsyncIterator(AbstractAsyncIterator):

    def __init__(self, client, event, *, timeout=None, check=None, limit=None):
        self._client = client
        self._event = event
        self._timeout = timeout
        self._check = check
        self._limit = limit
        self._count = 0

    async def next(self):
        if self._limit is not None:
            if self._count >= self._limit:
                raise NoMoreItems()
            self._count += 1
        item = await self._client.wait_for(self._event, timeout=self._timeout, check=self._check)
        return item