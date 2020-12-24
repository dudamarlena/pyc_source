# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/altered/contextdecorator.py
# Compiled at: 2017-02-23 02:57:46
"""
Create objects that act as both context managers *and* as decorators, and behave
the same in both cases.

Context managers inheriting from ``ContextDecorator`` have to implement
``__enter__`` and ``__exit__`` as normal. ``__exit__`` retains its optional
exception handling even when used as a decorator.

Example::

   from contextlib import ContextDecorator

   class mycontext(ContextDecorator):
      def __enter__(self):
         print 'Starting'
         return self

      def __exit__(self, *exc):
         print 'Finishing'
         return False

   @mycontext()
   def function():
      print 'The bit in the middle'

   with mycontext():
      print 'The bit in the middle'

Existing context managers that already have a base class can be extended by
using ``ContextDecorator`` as a mixin class::

   from contextlib import ContextDecorator

   class mycontext(ContextBaseClass, ContextDecorator):
      def __enter__(self):
         return self

      def __exit__(self, *exc):
         return False

"""
import sys
try:
    from functools import wraps
except ImportError:

    def wraps(original):

        def inner(f):
            f.__name__ = original.__name__
            return f

        return inner


if sys.version_info >= (3, 0):
    exec '\ndef _reraise(cls, val, tb):\n    raise val\n'
else:
    exec '\ndef _reraise(cls, val, tb):\n    raise cls, val, tb\n'
try:
    next
except NameError:

    def next(gen):
        return gen.next()


__all__ = ['__version__', 'ContextDecorator', 'contextmanager']
__version__ = '0.10.0'
_NO_EXCEPTION = (None, None, None)

class ContextDecorator(object):
    """A base class or mixin that enables context managers to work as decorators."""

    def __call__(self, f):

        @wraps(f)
        def inner(*args, **kw):
            self.__enter__()
            exc = _NO_EXCEPTION
            try:
                result = f(*args, **kw)
            except Exception:
                exc = sys.exc_info()

            catch = self.__exit__(*exc)
            if not catch and exc is not _NO_EXCEPTION:
                _reraise(*exc)
            return result

        return inner


class GeneratorContextManager(ContextDecorator):
    """Helper for @contextmanager decorator."""

    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield")

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                next(self.gen)
            except StopIteration:
                return

            raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = type()
            try:
                self.gen.throw(type, value, traceback)
                raise RuntimeError("generator didn't stop after throw()")
            except StopIteration:
                exc = sys.exc_info()[1]
                return exc is not value
            except:
                if sys.exc_info()[1] is not value:
                    raise

        return


def contextmanager(func):
    """@contextmanager decorator.

    Typical usage:

        @contextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>

    This makes this:

        with some_generator(<arguments>) as <variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>

    """

    @wraps(func)
    def helper(*args, **kwds):
        return GeneratorContextManager(func(*args, **kwds))

    return helper