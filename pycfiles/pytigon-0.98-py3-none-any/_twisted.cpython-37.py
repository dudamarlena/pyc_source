# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyee/pyee/_twisted.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 2455 bytes
from pyee._base import BaseEventEmitter
from twisted.internet.defer import Deferred, ensureDeferred
from twisted.python.failure import Failure
try:
    from asyncio import iscoroutine
except ImportError:
    iscoroutine = None

__all__ = [
 'TwistedEventEmitter']

class TwistedEventEmitter(BaseEventEmitter):
    __doc__ = 'An event emitter class which can run twisted coroutines and handle\n    returned Deferreds, in addition to synchronous blocking functions. For\n    example::\n\n        @ee.on(\'event\')\n        @inlineCallbacks\n        def async_handler(*args, **kwargs):\n            yield returns_a_deferred()\n\n    or::\n\n        @ee.on(\'event\')\n        async def async_handler(*args, **kwargs):\n            await returns_a_deferred()\n\n\n    When async handlers fail, Failures are first emitted on the ``failure``\n    event. If there are no ``failure`` handlers, the Failure\'s associated\n    exception is then emitted on the ``error`` event. If there are no ``error``\n    handlers, the exception is raised. For consistency, when handlers raise\n    errors synchronously, they\'re captured, wrapped in a Failure and treated\n    as an async failure. This is unlike the behavior of BaseEventEmitter,\n    which have no special error handling.\n\n    For twisted coroutine event handlers, calling emit is non-blocking.\n    In other words, you do not have to await any results from emit, and the\n    coroutine is scheduled in a fire-and-forget fashion.\n\n    Similar behavior occurs for "sync" functions which return Deferreds.\n    '

    def __init__(self):
        super(TwistedEventEmitter, self).__init__()

    def _emit_run(self, f, args, kwargs):
        try:
            result = f(*args, **kwargs)
        except Exception:
            self.emit('failure', Failure())
        else:
            if iscoroutine and iscoroutine(result):
                d = ensureDeferred(result)
            else:
                if isinstance(result, Deferred):
                    d = result
                else:
                    d = None
            if d:

                @d.addErrback
                def _errback(failure):
                    if failure:
                        self.emit('failure', failure)

    def _emit_handle_potential_error(self, event, error):
        if event == 'failure':
            self.emit('error', error.value)
        else:
            super(TwistedEventEmitter, self)._emit_handle_potential_error(event, error)