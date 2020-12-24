# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/filter.py
# Compiled at: 2011-04-22 17:53:28
"""
    pygments.filter
    ~~~~~~~~~~~~~~~

    Module that implements the default filter.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

def apply_filters(stream, filters, lexer=None):
    """
    Use this method to apply an iterable of filters to
    a stream. If lexer is given it's forwarded to the
    filter, otherwise the filter receives `None`.
    """

    def _apply(filter_, stream):
        for token in filter_.filter(lexer, stream):
            yield token

    for filter_ in filters:
        stream = _apply(filter_, stream)

    return stream


def simplefilter(f):
    """
    Decorator that converts a function into a filter::

        @simplefilter
        def lowercase(lexer, stream, options):
            for ttype, value in stream:
                yield ttype, value.lower()
    """
    return type(f.__name__, (FunctionFilter,), {'function': f, 
       '__module__': getattr(f, '__module__'), 
       '__doc__': f.__doc__})


class Filter(object):
    """
    Default filter. Subclass this class or use the `simplefilter`
    decorator to create own filters.
    """

    def __init__(self, **options):
        self.options = options

    def filter(self, lexer, stream):
        raise NotImplementedError()


class FunctionFilter(Filter):
    """
    Abstract class used by `simplefilter` to create simple
    function filters on the fly. The `simplefilter` decorator
    automatically creates subclasses of this class for
    functions passed to it.
    """
    function = None

    def __init__(self, **options):
        if not hasattr(self, 'function'):
            raise TypeError('%r used without bound function' % self.__class__.__name__)
        Filter.__init__(self, **options)

    def filter(self, lexer, stream):
        for (ttype, value) in self.function(lexer, stream, self.options):
            yield (
             ttype, value)