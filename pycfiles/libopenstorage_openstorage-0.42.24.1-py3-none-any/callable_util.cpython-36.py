# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/framework/foundation/callable_util.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 3151 bytes
"""Utilities for working with callables."""
import abc, collections, enum, functools, logging, six
_LOGGER = logging.getLogger(__name__)

class Outcome(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'A sum type describing the outcome of some call.\n\n  Attributes:\n    kind: One of Kind.RETURNED or Kind.RAISED respectively indicating that the\n      call returned a value or raised an exception.\n    return_value: The value returned by the call. Must be present if kind is\n      Kind.RETURNED.\n    exception: The exception raised by the call. Must be present if kind is\n      Kind.RAISED.\n  '

    @enum.unique
    class Kind(enum.Enum):
        __doc__ = 'Identifies the general kind of the outcome of some call.'
        RETURNED = object()
        RAISED = object()


class _EasyOutcome(collections.namedtuple('_EasyOutcome', [
 'kind', 'return_value', 'exception']), Outcome):
    __doc__ = 'A trivial implementation of Outcome.'


def _call_logging_exceptions(behavior, message, *args, **kwargs):
    try:
        return _EasyOutcome(Outcome.Kind.RETURNED, behavior(*args, **kwargs), None)
    except Exception as e:
        _LOGGER.exception(message)
        return _EasyOutcome(Outcome.Kind.RAISED, None, e)


def with_exceptions_logged(behavior, message):
    """Wraps a callable in a try-except that logs any exceptions it raises.

  Args:
    behavior: Any callable.
    message: A string to log if the behavior raises an exception.

  Returns:
    A callable that when executed invokes the given behavior. The returned
      callable takes the same arguments as the given behavior but returns a
      future.Outcome describing whether the given behavior returned a value or
      raised an exception.
  """

    @functools.wraps(behavior)
    def wrapped_behavior(*args, **kwargs):
        return _call_logging_exceptions(behavior, message, *args, **kwargs)

    return wrapped_behavior


def call_logging_exceptions(behavior, message, *args, **kwargs):
    """Calls a behavior in a try-except that logs any exceptions it raises.

  Args:
    behavior: Any callable.
    message: A string to log if the behavior raises an exception.
    *args: Positional arguments to pass to the given behavior.
    **kwargs: Keyword arguments to pass to the given behavior.

  Returns:
    An Outcome describing whether the given behavior returned a value or raised
      an exception.
  """
    return _call_logging_exceptions(behavior, message, *args, **kwargs)