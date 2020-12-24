# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/framework/foundation/logging_pool.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 2214 bytes
"""A thread pool that logs exceptions raised by tasks executed within it."""
import logging
from concurrent import futures
_LOGGER = logging.getLogger(__name__)

def _wrap(behavior):
    """Wraps an arbitrary callable behavior in exception-logging."""

    def _wrapping(*args, **kwargs):
        try:
            return behavior(*args, **kwargs)
        except Exception:
            _LOGGER.exception('Unexpected exception from %s executed in logging pool!', behavior)
            raise

    return _wrapping


class _LoggingPool(object):
    __doc__ = 'An exception-logging futures.ThreadPoolExecutor-compatible thread pool.'

    def __init__(self, backing_pool):
        self._backing_pool = backing_pool

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._backing_pool.shutdown(wait=True)

    def submit(self, fn, *args, **kwargs):
        return (self._backing_pool.submit)(_wrap(fn), *args, **kwargs)

    def map(self, func, *iterables, **kwargs):
        return (self._backing_pool.map)(
 _wrap(func), *iterables, **{'timeout': kwargs.get('timeout', None)})

    def shutdown(self, wait=True):
        self._backing_pool.shutdown(wait=wait)


def pool(max_workers):
    """Creates a thread pool that logs exceptions raised by the tasks within it.

  Args:
    max_workers: The maximum number of worker threads to allow the pool.

  Returns:
    A futures.ThreadPoolExecutor-compatible thread pool that logs exceptions
      raised by the tasks executed within it.
  """
    return _LoggingPool(futures.ThreadPoolExecutor(max_workers))