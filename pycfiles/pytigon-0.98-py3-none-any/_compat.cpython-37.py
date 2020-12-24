# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyee/pyee/_compat.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 2648 bytes
from pyee._base import BaseEventEmitter
from warnings import warn
try:
    from asyncio import iscoroutine, ensure_future
except ImportError:
    iscoroutine = None
    ensure_future = None

class CompatEventEmitter(BaseEventEmitter):
    __doc__ = 'An EventEmitter exposed for compatibility with prior versions of\n    pyee. This functionality is deprecated; you should instead use either\n    ``AsyncIOEventEmitter``, ``TwistedEventEmitter``, ``ExecutorEventEmitter``,\n    ``TrioEventEmitter`` or ``BaseEventEmitter``.\n\n    This class is similar to the ``AsyncIOEventEmitter`` class, but also allows\n    for overriding the scheduler function (``ensure_future`` by default as in\n    ``ASyncIOEventEmitter``) and does duck typing checks to handle Deferreds.\n    In other words, by setting ``scheduler`` to\n    ``twisted.internet.defer.ensureDeferred`` this will support twisted use\n    cases for coroutines.\n\n    When calling synchronous handlers, raised exceptions are ignored - as with\n    the BaseEventEmitter, you must capture and handle your own exceptions.\n    However, for coroutine functions, exceptions are handled by emitting them\n    on the ``error`` event.  Note that when using with twisted, the ``error``\n    event will emit Failures, not Exceptions.\n\n    This class will also successfully import in python 2, but without coroutine\n    support.\n    '

    def __init__(self, scheduler=ensure_future, loop=None):
        warn(DeprecationWarning('pyee.EventEmitter is deprecated and will be removed in a future major version; you should instead use either pyee.AsyncIOEventEmitter, pyee.TwistedEventEmitter, pyee.ExecutorEventEmitter, pyee.TrioEventEmitter, or pyee.BaseEventEmitter.'))
        super(CompatEventEmitter, self).__init__()
        self._schedule = scheduler
        self._loop = loop

    def _emit_run(self, f, args, kwargs):
        coro = f(*args, **kwargs)
        if iscoroutine:
            if iscoroutine(coro):
                if self._loop:
                    d = self._schedule(coro, loop=(self._loop))
                else:
                    d = self._schedule(coro)
                if hasattr(d, 'add_done_callback'):

                    @d.add_done_callback
                    def _callback(f):
                        exc = f.exception()
                        if exc:
                            self.emit('error', exc)

                else:
                    if hasattr(d, 'addErrback'):

                        @d.addErrback
                        def _callback(exc):
                            self.emit('error', exc)