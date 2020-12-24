# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/filter.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2038 bytes
"""
    pygments.filter
    ~~~~~~~~~~~~~~~

    Module that implements the default filter.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
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
        def lowercase(self, lexer, stream, options):
            for ttype, value in stream:
                yield ttype, value.lower()
    """
    return type(f.__name__, (FunctionFilter,), {'__module__':getattr(f, '__module__'), 
     '__doc__':f.__doc__, 
     'function':f})


class Filter(object):
    __doc__ = '\n    Default filter. Subclass this class or use the `simplefilter`\n    decorator to create own filters.\n    '

    def __init__(self, **options):
        self.options = options

    def filter(self, lexer, stream):
        raise NotImplementedError()


class FunctionFilter(Filter):
    __doc__ = '\n    Abstract class used by `simplefilter` to create simple\n    function filters on the fly. The `simplefilter` decorator\n    automatically creates subclasses of this class for\n    functions passed to it.\n    '
    function = None

    def __init__(self, **options):
        if not hasattr(self, 'function'):
            raise TypeError('%r used without bound function' % self.__class__.__name__)
        (Filter.__init__)(self, **options)

    def filter(self, lexer, stream):
        for ttype, value in self.function(lexer, stream, self.options):
            yield (
             ttype, value)