# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/utils.py
# Compiled at: 2008-03-07 17:28:21
from AccessControl.requestmethod import _buildFacade
import inspect
_default = []

def protect(callable, *checkers):
    spec = inspect.getargspec(callable)
    args, defaults = spec[0], spec[3]
    try:
        r_index = args.index('REQUEST')
    except ValueError:
        raise ValueError('No REQUEST parameter in callable signature')

    arglen = len(args)
    if defaults is not None:
        defaults = zip(args[arglen - len(defaults):], defaults)
        arglen -= len(defaults)

    def _curried(*args, **kw):
        request = None
        if len(args) > r_index:
            request = args[r_index]
        for checker in checkers:
            checker(request)

        if defaults is not None:
            args, kwparams = args[:arglen], args[arglen:]
            for (positional, (key, default)) in zip(kwparams, defaults):
                if positional is _default:
                    kw[key] = default
                else:
                    kw[key] = positional

        return callable(*args, **kw)

    facade_globs = dict(_curried=_curried, _default=_default)
    exec _buildFacade(spec, callable.__doc__) in facade_globs
    return facade_globs['_facade']