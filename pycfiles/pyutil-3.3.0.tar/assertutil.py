# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/assertutil.py
# Compiled at: 2019-06-26 11:58:00
"""
Tests useful in assertion checking, prints out nicely formated messages too.
"""
from .humanreadable import hr

def _format_error(prefix, args, kwargs):
    if prefix:
        msgbuf = [
         prefix]
        if args or kwargs:
            msgbuf.append(': ')
    else:
        msgbuf = []
    if args:
        msgbuf.append((', ').join([ '%s %s' % tuple(map(hr, (arg, type(arg)))) for arg in args ]))
    if kwargs:
        if args:
            msgbuf.append(', ')
        msgbuf.append((', ').join([ '%s: %s %s' % tuple(map(hr, (k, kwargs[k], type(kwargs[k])))) for k in sorted(kwargs.keys()) ]))
    return ('').join(msgbuf)


def _assert(___cond=False, *args, **kwargs):
    if ___cond:
        return True
    else:
        raise AssertionError(_format_error(None, args, kwargs))
        return


def precondition(___cond=False, *args, **kwargs):
    if ___cond:
        return True
    raise AssertionError(_format_error('precondition', args, kwargs))


def postcondition(___cond=False, *args, **kwargs):
    if ___cond:
        return True
    raise AssertionError(_format_error('postcondition', args, kwargs))