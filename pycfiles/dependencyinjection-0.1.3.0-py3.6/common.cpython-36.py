# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\common.py
# Compiled at: 2018-01-24 01:54:31
# Size of source mod 2**32: 1709 bytes
from abc import abstractmethod, abstractproperty
from enum import Enum

class LifeTime(Enum):
    singleton = 0
    scoped = 1
    transient = 2


class IServiceProvider:

    def get(self, service_type: type):
        """
        get service by the type.
        """
        raise NotImplementedError

    def scope(self):
        """
        get a scoped `IServiceProvider`.

        usage:
        ``` py
        with ?.scope() as service_provider:
            obj = service_provider.get(?)
        ```
        """
        raise NotImplementedError


class ICallSiteMaker:

    @abstractmethod
    def make_callsite(self, service_provider: IServiceProvider, depend_chain):
        """create a callsite."""
        raise NotImplementedError


class IDescriptor(ICallSiteMaker):

    @abstractproperty
    def service_type(self) -> type:
        raise NotImplementedError

    @abstractproperty
    def lifetime(self) -> LifeTime:
        raise NotImplementedError


class IScopedFactory:

    @property
    def service_provider(self):
        raise NotImplementedError


class ILock:
    __doc__ = ' the lock use for scoped service provider. '

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError


class FakeLock(ILock):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


FAKE_LOCK = FakeLock()