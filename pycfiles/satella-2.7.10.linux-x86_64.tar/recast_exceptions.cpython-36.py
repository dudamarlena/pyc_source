# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/recast_exceptions.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 7640 bytes
import typing as tp, logging, threading
from .decorators import wraps
__all__ = [
 'rethrow_as',
 'silence_excs',
 'catch_exception',
 'log_exceptions']
ExcType = tp.Type[Exception]
T = tp.TypeVar('T')

def silence_excs(*exc_types: ExcType, returns=None):
    """
    Silence given exception types.

    Can be either a decorator or a context manager.

    If you are using it as a decorator, you can specify what value should the function return
    by using the returns kwarg:

    >>> @silence_excs(KeyError, returns=5)
    >>> def returns_5():
    >>>     raise KeyError()
    >>> assert returns_5() == 5
    """
    return rethrow_as(exc_types, None, returns=returns)


class log_exceptions:
    __doc__ = '\n    Decorator/context manager to log your exceptions into the log.\n\n    The exception will be logged and re-raised.\n\n    Logger will be passed the exception instance as exc_info.\n\n    :param logger: a logger to which the exception has to be logged\n    :param severity: a severity level\n    :param format_string: a format string with fields:\n        - e      : the exception instance itself\n        - args   : arguments with which the function was called, unavailable if context manager\n        - kwargs : arguments with which the function was called, unavailable if context manager\n        You can specify additional fields providing the locals_ argument\n        Example: "{exc_type} occurred with message {exc_val} with traceback {exc_tb}"\n    :param locals_: local variables to add to the format string. args and kwargs will be overwritten\n        by this, but e will never be overwritten.\n    :param exc_types: logger will log only on those exceptions. Default is None which means\n        log on all exceptions\n    '
    __slots__ = ('logger', 'severity', 'format_string', 'locals', 'exc_types')

    def __init__(self, logger, severity=logging.ERROR, format_string='{exc_val}', locals_: tp.Optional[tp.Dict]=None, exc_types: tp.Optional[tp.Union[(ExcType, tp.Sequence[ExcType])]]=None):
        self.logger = logger
        self.severity = severity
        self.format_string = format_string
        self.locals = locals_
        if exc_types is None:
            self.exc_types = Exception
        else:
            self.exc_types = exc_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if issubclass(exc_type, self.exc_types):
                format_dict = {}
                if self.locals is not None:
                    format_dict.update(self.locals)
                format_dict['e'] = exc_val
                self.logger.log((self.severity), (self.format_string.format(format_dict)), exc_info=exc_val)
        return False

    def __call__(self, fun):

        @wraps(fun)
        def inner(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except Exception as e:
                if isinstance(e, self.exc_types):
                    format_dict = {'args':args, 
                     'kwargs':kwargs}
                    if self.locals is not None:
                        format_dict.update(self.locals)
                    format_dict['e'] = e
                    self.logger.log((self.severity), (self.format_string.format(format_dict)), exc_info=e)
                raise e

        return inner


class rethrow_as:
    __doc__ = '\n    Transform some exceptions into others.\n\n    Either a decorator or a context manager\n\n    New exception will be created by calling exception to transform to with\n    repr of current one.\n\n    You can also provide just two exceptions, eg.\n\n    >>> rethrow_as(NameError, ValueError)\n\n    You can also provide a pairwise translation, eg. from NameError to ValueError and from OSError\n    to IOError\n\n    >>> rethrow_as((NameError, ValueError), (OSError, IOError))\n\n    If the second value is a None, exception will be silenced.\n    '
    __slots__ = ('mapping', 'exception_preprocessor', 'returns', '__exception_remapped')

    def __init__(self, *pairs: tp.Union[(ExcType, tp.Tuple[(ExcType, ExcType)])], exception_preprocessor: tp.Optional[tp.Callable[([Exception], str)]]=repr, returns=None):
        """
        Pass tuples of (exception to catch - exception to transform to).

        :param exception_preprocessor: other callable/1 to use instead of repr.
            Should return a str, a text description of the exception
        :param returns: what value should the function return if this is used as a decorator
        """
        try:
            a, b = pairs
            op = issubclass(b, BaseException)
        except TypeError:
            op = b is None
        except ValueError:
            op = False

        if op:
            pairs = [
             pairs]
        self.mapping = list(pairs)
        self.exception_preprocessor = exception_preprocessor or repr
        self.returns = returns
        self._rethrow_as__exception_remapped = threading.local()

    def __call__(self, fun: tp.Callable) -> tp.Callable:

        @wraps(fun)
        def inner(*args, **kwargs):
            with self:
                v = fun(*args, **kwargs)
            if self._rethrow_as__exception_remapped.was_raised:
                return self.returns
            else:
                return v

        return inner

    def __enter__(self):
        self._rethrow_as__exception_remapped.was_raised = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            for from_, to in self.mapping:
                if issubclass(exc_type, from_):
                    self._rethrow_as__exception_remapped.was_raised = True
                    if to is None:
                        return True
                    raise to(self.exception_preprocessor(exc_val))


def catch_exception(exc_class: tp.Union[(ExcType, tp.Tuple[ExcType])], clb: tp.Callable[([], T)], return_instead: tp.Optional[T]=None, return_value_on_no_exception: bool=False) -> tp.Union[(Exception, T)]:
    """
    Catch exception of given type and return it. Functionally equivalent to:

    >>> try:
    >>>     v = clb()
    >>>     if return_value_on_no_exception:
    >>>         return v
    >>> except exc_class as e:
    >>>     if return_instead:
    >>>         return return_instead
    >>>     return e

    :param exc_class: Exception classes to catch
    :param clb: callable/0 to call to raise the exception
    :param return_instead: what to return instead of the function result if it didn't end in an
        exception
    :param return_value_on_no_exception: whether to return the function result if exception didn't
        happen
    :raises ValueError: an exception was not thrown
    :raises TypeError: a different exception was thrown that the one we're catchin
    """
    try:
        result = clb()
    except exc_class as e:
        return e
    except Exception as e:
        raise TypeError('%s was thrown instead' % (e,))

    if return_instead is not None:
        return return_instead
    if return_value_on_no_exception:
        return result
    raise ValueError('Callable executed without error')