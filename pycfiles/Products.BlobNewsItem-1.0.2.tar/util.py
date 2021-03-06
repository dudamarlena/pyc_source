# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteDeploy-1.5.0-py2.6.egg/paste/deploy/util.py
# Compiled at: 2012-02-27 07:41:55
import inspect, sys
from paste.deploy.compat import reraise

def fix_type_error(exc_info, callable, varargs, kwargs):
    """
    Given an exception, this will test if the exception was due to a
    signature error, and annotate the error with better information if
    so.

    Usage::

      try:
          val = callable(*args, **kw)
      except TypeError:
          exc_info = fix_type_error(None, callable, args, kw)
          raise exc_info[0], exc_info[1], exc_info[2]
    """
    if exc_info is None:
        exc_info = sys.exc_info()
    if exc_info[0] != TypeError or str(exc_info[1]).find('arguments') == -1 or getattr(exc_info[1], '_type_error_fixed', False):
        return exc_info
    else:
        exc_info[1]._type_error_fixed = True
        argspec = inspect.formatargspec(*inspect.getargspec(callable))
        args = (', ').join(map(_short_repr, varargs))
        if kwargs and args:
            args += ', '
        if kwargs:
            kwargs = kwargs.items()
            kwargs.sort()
            args += (', ').join([ '%s=...' % n for (n, v) in kwargs ])
        gotspec = '(%s)' % args
        msg = '%s; got %s, wanted %s' % (exc_info[1], gotspec, argspec)
        exc_info[1].args = (msg,)
        return exc_info


def _short_repr(v):
    v = repr(v)
    if len(v) > 12:
        v = v[:8] + '...' + v[-4:]
    return v


def fix_call(callable, *args, **kw):
    """
    Call ``callable(*args, **kw)`` fixing any type errors that come out.
    """
    try:
        val = callable(*args, **kw)
    except TypeError:
        exc_info = fix_type_error(None, callable, args, kw)
        reraise(*exc_info)

    return val


def lookup_object(spec):
    """
    Looks up a module or object from a some.module:func_name specification.
    To just look up a module, omit the colon and everything after it.
    """
    (parts, target) = spec.split(':') if ':' in spec else (spec, None)
    module = __import__(parts)
    for part in parts.split('.')[1:] + ([target] if target else []):
        module = getattr(module, part)

    return module