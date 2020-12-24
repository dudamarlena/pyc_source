# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/inspector.py
# Compiled at: 2009-06-08 07:12:47
import inspect

def print_func(func):
    print
    call = format_args(func)
    cmt = inspect.getcomments(func)
    if cmt:
        print cmt
    print '%s(%s)' % (func.__name__, call)
    doc = inspect.getdoc(func)
    if doc:
        print doc
    print


def format_args(func):
    try:
        return _format_args(func)
    except:
        return '...'


def _format_args(func):
    (args, pargs, kargs, defs) = inspect.getargspec(func)
    sep = len(args) - len(defs)
    funcargs = args[:sep] + map(lambda x, y: x + '=' + `y`, args[sep:], defs or ())
    if pargs:
        funcargs.append('*' + pargs)
    if kargs:
        funcargs.append('**' + kargs)
    return (', ').join(funcargs)


def print_source_func(func):
    print
    comment = inspect.getcomments(func)
    if comment:
        print comment
    try:
        print inspect.getsource(func)
    except:
        args = format_args(func)
        print 'def %s(%s):' % (func.__name__, args)
        print '\t<...>'

    print