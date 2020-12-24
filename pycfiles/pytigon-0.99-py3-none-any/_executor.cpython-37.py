# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/pyee/pyee/_executor.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 2200 bytes
from pyee._base import BaseEventEmitter
try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    from futures import ThreadPoolExecutor

__all__ = [
 'ExecutorEventEmitter']

class ExecutorEventEmitter(BaseEventEmitter):
    __doc__ = "An event emitter class which runs handlers in a ``concurrent.futures``\n    executor. If using python 2, this will fall back to trying to use the\n    ``futures`` backported library (caveats there apply).\n\n    By default, this class creates a default ``ThreadPoolExecutor``, but\n    a custom executor may also be passed in explicitly to, for instance,\n    use a ``ProcessPoolExecutor`` instead.\n\n    This class runs all emitted events on the configured executor. Errors\n    captured by the resulting Future are automatically emitted on the\n    ``error`` event. This is unlike the BaseEventEmitter, which have no error\n    handling.\n\n    The underlying executor may be shut down by calling the ``shutdown``\n    method. Alternately you can treat the event emitter as a context manager::\n\n        with ExecutorEventEmitter() as ee:\n            # Underlying executor open\n\n            @ee.on('data')\n            def handler(data):\n                print(data)\n\n            ee.emit('event')\n\n        # Underlying executor closed\n\n    Since the function call is scheduled on an executor, emit is always\n    non-blocking.\n\n    No effort is made to ensure thread safety, beyond using an executor.\n    "

    def __init__(self, executor=None):
        super(ExecutorEventEmitter, self).__init__()
        if executor:
            self._executor = executor
        else:
            self._executor = ThreadPoolExecutor()

    def _emit_run(self, f, args, kwargs):
        future = (self._executor.submit)(f, *args, **kwargs)

        @future.add_done_callback
        def _callback(f):
            exc = f.exception()
            if exc:
                self.emit('error', exc)

    def shutdown(self, wait=True):
        """Call ``shutdown`` on the internal executor."""
        self._executor.shutdown(wait=wait)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.shutdown()