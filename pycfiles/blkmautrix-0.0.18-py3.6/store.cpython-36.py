# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/store.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1105 bytes
from typing import Optional
from abc import ABC, abstractmethod
from .api.types import SyncToken

class ClientStore(ABC):
    __doc__ = 'ClientStore persists high-level client stuff.'

    @property
    @abstractmethod
    def next_batch(self) -> SyncToken:
        return SyncToken('')

    @next_batch.setter
    @abstractmethod
    def next_batch(self, value: SyncToken) -> None:
        pass


class MemoryClientStore(ClientStore):
    __doc__ = 'MemoryClientStore is a :class:`ClientStore` implementation that stores the data in memory.'

    def __init__(self, next_batch: Optional[SyncToken]=None) -> None:
        self._next_batch = next_batch

    @property
    def next_batch(self) -> Optional[SyncToken]:
        return self._next_batch

    @next_batch.setter
    def next_batch(self, value: SyncToken) -> None:
        self._next_batch = value