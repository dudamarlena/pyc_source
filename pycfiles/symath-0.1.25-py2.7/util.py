# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/util.py
# Compiled at: 2015-08-21 11:58:24
import symath.core, pprint
DEBUG = False

def pretty(exp):
    p = pprint.PrettyPrinter(indent=2)
    p.pprint(exp)


def debug(exp):
    if DEBUG:
        if type(exp) == type('str'):
            print exp
        else:
            pretty(exp)


def dict_reverse(d):
    rv = {}
    for k in d:
        rv[d[k]] = k

    return rv


def has_wilds(exp):
    rv = {}
    rv['val'] = False

    def _(exp):
        if isinstance(exp, symath.core.Wild):
            rv['val'] = True
        return exp

    exp.walk(_)
    return rv['val']