# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/louieck/robustapply.py
# Compiled at: 2018-05-31 10:36:55
"""Robust apply mechanism.

Provides a function 'call', which can sort out what arguments a given
callable object can take, and subset the given arguments to match only
those which are acceptable.
"""
import sys
if sys.hexversion >= 50331648:
    IM_FUNC = '__func__'
    FUNC_CODE = '__code__'
else:
    IM_FUNC = 'im_func'
    FUNC_CODE = 'func_code'

def function(receiver):
    """Get function-like callable object for given receiver.

    returns (function_or_method, codeObject, fromMethod)

    If fromMethod is true, then the callable already has its first
    argument bound.
    """
    if hasattr(receiver, IM_FUNC):
        im_func = getattr(receiver, IM_FUNC)
        func_code = getattr(im_func, FUNC_CODE)
        return (
         receiver, func_code, True)
    if hasattr(receiver, FUNC_CODE):
        func_code = getattr(receiver, FUNC_CODE)
        return (
         receiver, func_code, False)
    if hasattr(receiver, '__call__'):
        return function(receiver.__call__)
    raise ValueError(('unknown reciever type {} {}').format(receiver, type(receiver)))


def robust_apply(receiver, signature, *arguments, **named):
    """Call receiver with arguments and appropriate subset of named.
    ``signature`` is the callable used to determine the call signature
    of the receiver, in case ``receiver`` is a callable wrapper of the
    actual receiver."""
    signature, code_object, startIndex = function(signature)
    acceptable = code_object.co_varnames[startIndex + len(arguments):code_object.co_argcount]
    for name in code_object.co_varnames[startIndex:startIndex + len(arguments)]:
        if name in named:
            raise TypeError(('Argument {0!r} specified both positionally and as a keyword for calling {1!r}').format(name, signature))

    if not code_object.co_flags & 8:
        for arg in list(named.keys()):
            if arg not in acceptable:
                del named[arg]

    return receiver(*arguments, **named)