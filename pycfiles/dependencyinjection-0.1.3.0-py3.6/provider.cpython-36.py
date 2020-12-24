# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\provider.py
# Compiled at: 2018-01-24 01:54:24
# Size of source mod 2**32: 4403 bytes
import contextlib, typing
from .common import IServiceProvider, IScopedFactory, ILock, FAKE_LOCK
from .descriptors import ListedDescriptor, ICallSiteMaker
from .servicesmap import ServicesMap
from .checker import CycleChecker
from .errors import TypeNotFoundError
from .callsites import LifeTimeCallSite
INTERNAL_TYPES = set([
 IServiceProvider,
 ILock])

class ServiceProvider(IServiceProvider):

    def __init__(self, parent_provider: IServiceProvider=None, service_map: ServicesMap=None):
        self._root_provider = parent_provider.root_provider if parent_provider else self
        self._exit_stack = contextlib.ExitStack()
        self._exit_stack.__enter__()
        self._service_map = service_map or parent_provider._service_map
        self._cache_list = {}
        self._callsites = {}
        self._lock = FAKE_LOCK
        if self._root_provider is self:
            self._lock = self.get(ILock)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._exit_stack.__exit__(exc_type, exc_value, traceback)
        self._cache_list.clear()

    @property
    def root_provider(self):
        return self._root_provider

    def __getitem__(self, service_type: type):
        return self._get(service_type, True)

    def get(self, service_type: type):
        return self._get(service_type, False)

    def _get(self, service_type: type, required):
        if not isinstance(service_type, type):
            raise TypeError
        callsite = self.get_callsite(service_type, None, required=required)
        if callsite:
            return callsite.get(self)

    def get_callsite(self, target: (type, ICallSiteMaker), depend_chain: CycleChecker, *, required=True):
        """ get or create callsite. """
        assert target is not None
        with self._lock:
            callsite = self._callsites.get(target)
            if callsite is None:
                if self is not self._root_provider:
                    callsite = self._root_provider.get_callsite(target, depend_chain)
                else:
                    if isinstance(target, type):
                        callsite = self._get_callsite_from_service_type(target, depend_chain, required=required)
                    else:
                        callsite = self._get_callsite_from_descriptor(target, depend_chain)
                self._callsites[target] = callsite
            return callsite

    def _get_callsite_from_service_type(self, service_type, depend_chain, *, required):
        descriptor = self._service_map.get(service_type)
        if descriptor:
            return self.get_callsite(descriptor, depend_chain)
        if getattr(service_type, '__origin__', None) is typing.List:
            if isinstance(service_type.__args__, tuple):
                inner_type, = service_type.__args__
                descriptors = self._service_map.getall(inner_type) or []
                return self.get_callsite(ListedDescriptor(descriptors), depend_chain)
        if required:
            raise TypeNotFoundError(f"cannot get type: {service_type}")

    def _get_callsite_from_descriptor(self, descriptor, depend_chain):
        return self.make_callsite(descriptor, depend_chain, from_type=(not isinstance(descriptor, ListedDescriptor)))

    def make_callsite(self, descriptor, depend_chain: CycleChecker, *, from_type=True):
        if self is not self._root_provider:
            return self._root_provider.make_callsite(descriptor, depend_chain)
        with self._lock:
            if depend_chain is None:
                depend_chain = CycleChecker()
            context = depend_chain.add_or_raise(descriptor.service_type) if from_type else FAKE_LOCK
            with context:
                callsite = descriptor.make_callsite(self, depend_chain)
                callsite = LifeTimeCallSite.wrap(descriptor, callsite)
                return callsite

    def scope(self):
        return self.get(IScopedFactory).service_provider