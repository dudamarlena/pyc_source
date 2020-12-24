# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/marrow/script/util.py
# Compiled at: 2010-11-24 19:49:55
import sys, types, inspect
from textwrap import wrap as wrap_
__all__ = [
 'wrap', 'InspectionComplete', 'InspectionFailed', 'getargspec']

def wrap(text, columns=78):
    lines = []
    if isinstance(text, list):
        in_paragraph = False
        for line in text:
            if not line:
                in_paragraph = False
                lines.append(line)
                continue
            if in_paragraph:
                lines[-1] = lines[(-1)] + ' ' + line
                continue
            lines.append(line)
            in_paragraph = True

        text = ('\n').join(lines)
        lines = []
    in_paragraph = True
    for iline in text.splitlines():
        if not iline:
            lines.append(iline)
        else:
            for oline in wrap_(iline, columns):
                lines.append(oline)

    return ('\n').join(lines)


class InspectionComplete(Exception):
    pass


class InspectionFailed(Exception):
    pass


def getargspec(obj):
    """An improved inspect.getargspec.
    
    Has a slightly different return value from the default getargspec.
    
    Returns a tuple of:
        required, optional, args, kwargs
        list, dict, bool, bool
    
    Required is a list of required named arguments.
    Optional is a dictionary mapping optional arguments to defaults.
    Args and kwargs are True for the respective unlimited argument type.
    """
    (argnames, varargs, varkw, _defaults) = (None, None, None, None)
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        (argnames, varargs, varkw, _defaults) = inspect.getargspec(obj)
    elif inspect.isclass(obj):
        if inspect.ismethoddescriptor(obj.__init__):
            (argnames, varargs, varkw, _defaults) = ([], False, False, None)
        else:
            (argnames, varargs, varkw, _defaults) = inspect.getargspec(obj.__init__)
    elif hasattr(obj, '__call__'):
        (argnames, varargs, varkw, _defaults) = inspect.getargspec(obj.__call__)
    else:
        raise TypeError('Object not callable?')
    if argnames and argnames[0] == 'self':
        del argnames[0]
    if _defaults is None:
        _defaults = []
        defaults = dict()
    else:
        defaults = dict()
        _defaults = list(_defaults)
        _defaults.reverse()
        argnames.reverse()
        for (i, default) in enumerate(_defaults):
            defaults[argnames[i]] = default

        argnames.reverse()
    return (
     argnames, defaults, True if varargs else False, True if varkw else False)