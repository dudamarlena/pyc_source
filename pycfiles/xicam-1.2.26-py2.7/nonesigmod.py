# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\modpkgs\nonesigmod.py
# Compiled at: 2018-08-27 17:21:06
_PYSIDE_NONE_SENTINEL = object()

def pyside_none_wrap(var):
    """None -> sentinel. Wrap this around out-of-thread emitting."""
    if var is None:
        return _PYSIDE_NONE_SENTINEL
    else:
        return var


def pyside_none_deco(func):
    """sentinel -> None. Decorate callbacks that react to out-of-thread
    signal emitting.

    Modifies the function such that any sentinels passed in
    are transformed into None.
    """

    def sentinel_guard(arg):
        if arg is _PYSIDE_NONE_SENTINEL:
            return None
        else:
            return arg

    def inner(*args, **kwargs):
        newargs = map(sentinel_guard, args)
        newkwargs = {k:sentinel_guard(v) for k, v in kwargs.iteritems()}
        return func(*newargs, **newkwargs)

    return inner