# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/who_calls.py
# Compiled at: 2004-05-24 13:56:39
import string, sys
from log import *
whoCallsError = 'whoCallsError'

def test():
    for i in range(1, 1000):
        pretty_who_calls()

    print_top_100()


def who_calls_helper():
    tinfo = []
    exc_info = sys.exc_info()
    f = exc_info[2].tb_frame.f_back
    while f:
        tinfo.append((f.f_code.co_filename, f.f_code.co_name, f.f_lineno))
        f = f.f_back

    del exc_info
    return tinfo


def who_calls():
    try:
        raise whoCallsError
    except whoCallsError:
        tinfo = who_calls_helper()

    return tinfo


def pretty_who_calls(strip=0):
    info = who_calls()
    buf = []
    for (file, function, line) in info[1 + strip:]:
        buf.append('   %s(%s): %s()' % (file, line, function))

    return string.join(buf, '\n')


def compact_traceback():
    (t, v, tb) = sys.exc_info()
    tbinfo = []
    if tb is None:
        return (
         (
          '', '', ''), str(t), str(v), 'traceback is None!!!')
    while 1:
        tbinfo.append(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name, str(tb.tb_lineno))
        tb = tb.tb_next
        if not tb:
            break

    del tb
    (file, function, line) = tbinfo[(-1)]
    info = '[' + string.join(map(lambda x: string.join(x, '|'), tbinfo), '] [') + ']'
    return (
     (
      file, function, line), str(t), str(v), info)
    return


import sys, types

def real_get_refcounts(base=None, set_base=0):
    d = {}
    sys.modules
    for (modname, m) in sys.modules.items():
        for sym in dir(m):
            o = getattr(m, sym)
            if type(o) is types.ClassType:
                name = '%s:%s' % (modname, o.__name__)
                cnt = sys.getrefcount(o)
                if base:
                    if set_base:
                        base[name] = cnt
                    elif cnt > base.get(name, 0):
                        d[name] = cnt - base.get(name, 0)
                else:
                    d[name] = cnt

    return d


def get_refcounts(base=None):
    d = real_get_refcounts(base=base)
    pairs = map(lambda x: (x[1], x[0]), d.items())
    pairs.sort()
    pairs.reverse()
    return pairs


REFCOUNTS = {}

def set_refcount_base():
    global REFCOUNTS
    real_get_refcounts(REFCOUNTS, set_base=1)


def print_top_100():
    print_top_N(100)


def print_top_N(N):
    for (n, c) in get_refcounts(REFCOUNTS)[:N]:
        log('%10d %s' % (n, c))