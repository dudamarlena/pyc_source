# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyee/pyee/_trio.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 3404 bytes
from contextlib import asynccontextmanager
import trio
from pyee._base import BaseEventEmitter, PyeeException
__all__ = [
 'TrioEventEmitter']

class TrioEventEmitter(BaseEventEmitter):
    __doc__ = "An event emitter class which can run trio tasks in a trio nursery.\n\n    By default, this class will lazily create both a nursery manager (the\n    object returned from ``trio.open_nursery()`` and a nursery (the object\n    yielded by using the nursery manager as an async context manager). It is\n    also possible to supply an existing nursery manager via the ``manager``\n    argument, or an existing nursery via the ``nursery`` argument.\n\n    Instances of TrioEventEmitter are themselves async context managers, so\n    that they may manage the lifecycle of the underlying trio nursery. For\n    example, typical usage of this library may look something like this::\n\n        async with TrioEventEmitter() as ee:\n            # Underlying nursery is instantiated and ready to go\n            @ee.on('data')\n            async def handler(data):\n                print(data)\n\n            ee.emit('event')\n\n        # Underlying nursery and manager have been cleaned up\n\n    Unlike the case with the BaseEventEmitter, all exceptions raised by event\n    handlers are automatically emitted on the ``error`` event. This is\n    important for trio coroutines specifically but is also handled for\n    synchronous functions for consistency.\n\n    For trio coroutine event handlers, calling emit is non-blocking. In other\n    words, you should not attempt to await emit; the coroutine is scheduled\n    in a fire-and-forget fashion.\n    "

    def __init__(self, nursery=None, manager=None):
        super(TrioEventEmitter, self).__init__()
        if nursery:
            if manager:
                raise PyeeException('You may either pass a nursery or a nursery manager but not both')
            self._nursery = nursery
            self._manager = None
        else:
            if manager:
                self._nursery = None
                self._manager = manager
            else:
                self._manager = trio.open_nursery()

    def _async_runner(self, f, args, kwargs):

        async def runner():
            try:
                await f(*args, **kwargs)
            except Exception as exc:
                try:
                    self.emit('error', exc)
                finally:
                    exc = None
                    del exc

        return runner

    def _emit_run(self, f, args, kwargs):
        self._nursery.start_soon(self._async_runner(f, args, kwargs))

    @asynccontextmanager
    async def context(self):
        """Returns an async contextmanager which manages the underlying
        nursery to the EventEmitter. The ``TrioEventEmitter``'s
        async context management methods are implemented using this
        function, but it may also be used directly for clarity.
        """
        if getattr(self, '_nursery', None):
            yield self._nursery
        else:
            async with self._manager as nursery:
                self._nursery = nursery
                yield self

    async def __aenter__(self):
        self._context = self.context()
        return await self._context.__aenter__()

    async def __aexit__(self, type, value, traceback):
        rv = await self._context.__aexit__(type, value, traceback)
        self._context = None
        self._nursery = None
        self._manager = None
        return rv