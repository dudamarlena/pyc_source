# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anodi/tools.py
# Compiled at: 2013-02-13 12:50:07
from backports import inspect
from anodi import annotated, empty
import re
_typenames = {}

class TypeName(object):
    """
    Expose a `__repr__` around `typeobj` to return a (best-effort)
    "meaningful" name (e.g., for writing function signatures).
    """

    def __init__(self, typeobj):
        self.typeobj = typeobj
        if hasattr(self.typeobj, '__name__'):
            self.repr = self.typeobj.__name__
        elif isinstance(self.typeobj, basestring):
            self.repr = self.typeobj
        else:
            self.repr = repr(self.typeobj)

    def __repr__(self):
        return self.repr


def typename(t):
    """
    Caching wrapper around :class:`TypeName`.
    """
    if t not in _typenames:
        _typenames[t] = TypeName(t)
    return _typenames[t]


_re_function_repr = re.compile('\n<[^\\>]*\nfunction \\s+\n(?P<name>[^\\s\\>]+)\n[^\\>]* \\>', re.UNICODE | re.VERBOSE)
_re_leading_ws = re.compile('^ (?P<indent> [ \\t]+) [^\\s]+', re.UNICODE | re.VERBOSE | re.MULTILINE)

def document(func):
    """
    Decorator to insert an annotated function signature into the
    docstring.
    """
    sig = inspect.signature(func)
    sigstr = '%s %s' % (func.__name__, sig)
    sigstr = _re_function_repr.sub('\\g<name>', sigstr)
    if func.__doc__ is None:
        func.__doc__ = ''
    else:
        m = _re_leading_ws.search(func.__doc__)
        if m:
            sigstr = m.group('indent') + sigstr
    func.__doc__ = sigstr + '\n\n' + func.__doc__
    return func