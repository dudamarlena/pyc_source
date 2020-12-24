# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/stuf/patterns.py
# Compiled at: 2014-12-18 18:07:56
"""stuf search."""
from os import sep
from functools import partial
from parse import compile as pcompile
from .utils import lru
from .base import first
from .six.moves import filterfalse
from .six import isstring, filter, map, rcompile, rescape, rsub

def globpattern(expr):
    """Translate glob `expr` to regular expression."""
    i, n = 0, len(expr)
    res = []
    rappend = res.append
    while i < n:
        c = expr[i]
        i += 1
        if c == '*':
            rappend('(.*)')
        elif c == '?':
            rappend('(.)')
        elif c == '[':
            j = i
            if j < n and expr[j] == '!':
                j += 1
            if j < n and expr[j] == ']':
                j += 1
            while j < n and expr[j] != ']':
                j += 1

            if j >= n:
                rappend('\\[')
            else:
                stuff = expr[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                rappend(('[{0}]').format(stuff))
        else:
            rappend(rescape(c))

    rappend('\\Z(?ms)')
    return rsub('((?<!\\\\)(\\\\\\\\)*)\\.', ('\\1[^{0}]').format('\\\\\\\\' if sep == '\\' else sep), ('').join(res))


regex = lambda expr, flag: rcompile(expr, flag).search
parse = lambda expr, flag: pcompile(expr)._search_re.search
glob = lambda expr, flag: rcompile(globpattern(expr), flag).search
SEARCH = dict(parse=parse, glob=glob, regex=regex)

@lru()
def searcher(expr, flags=32):
    """Build search function from `expr`."""
    try:
        (scheme, expr) = expr.split(':', 1) if isstring(expr) else expr
        return SEARCH[scheme](expr, flags)
    except KeyError:
        raise TypeError(('"{0}" is invalid search scheme').format(scheme))


def detect(patterns):
    """Match item in sequence with pattern in `patterns`."""
    return partial(lambda y, x: any(p(first(x)) for p in y), tuple(map(searcher, patterns)))


def _clude(filter, default, patterns):
    """Create filter from `patterns`."""
    if not patterns:
        return default
    patterns = tuple(map(searcher, patterns))
    return partial(filter, lambda x: any(p(x) for p in patterns))


exclude = partial(_clude, filterfalse, lambda x: x)
include = partial(_clude, filter, lambda x: x[0:0])