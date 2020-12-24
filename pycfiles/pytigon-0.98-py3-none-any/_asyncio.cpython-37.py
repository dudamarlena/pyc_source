# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyee/pyee/_asyncio.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 2155 bytes
from asyncio import ensure_future, Future, iscoroutine
from pyee._base import BaseEventEmitter
__all__ = [
 'AsyncIOEventEmitter']

class AsyncIOEventEmitter(BaseEventEmitter):
    __doc__ = "An event emitter class which can run asyncio coroutines in addition to\n    synchronous blocking functions. For example::\n\n        @ee.on('event')\n        async def async_handler(*args, **kwargs):\n            await returns_a_future()\n\n    On emit, the event emitter  will automatically schedule the coroutine using\n    ``asyncio.ensure_future`` and the configured event loop (defaults to\n    ``asyncio.get_event_loop()``).\n\n    Unlike the case with the BaseEventEmitter, all exceptions raised by\n    event handlers are automatically emitted on the ``error`` event. This is\n    important for asyncio coroutines specifically but is also handled for\n    synchronous functions for consistency.\n\n    When ``loop`` is specified, the supplied event loop will be used when\n    scheduling work with ``ensure_future``. Otherwise, the default asyncio\n    event loop is used.\n\n    For asyncio coroutine event handlers, calling emit is non-blocking.\n    In other words, you do not have to await any results from emit, and the\n    coroutine is scheduled in a fire-and-forget fashion.\n    "

    def __init__(self, loop=None):
        super(AsyncIOEventEmitter, self).__init__()
        self._loop = loop

    def _emit_run(self, f, args, kwargs):
        try:
            coro = f(*args, **kwargs)
        except Exception as exc:
            try:
                self.emit('error', exc)
            finally:
                exc = None
                del exc

        else:
            if iscoroutine(coro):
                if self._loop:
                    f = ensure_future(coro, loop=(self._loop))
                else:
                    f = ensure_future(coro)
            elif isinstance(coro, Future):
                f = coro
            else:
                f = None
            if f:

                @f.add_done_callback
                def _callback(f):
                    if f.cancelled():
                        return
                    exc = f.exception()
                    if exc:
                        self.emit('error', exc)