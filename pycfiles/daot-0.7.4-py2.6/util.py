# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\util.py
# Compiled at: 2011-10-18 23:43:28
from dao.term import Var, DummyVar
(k, x, y, z, n, i, j) = (
 Var('k'), Var('x'), Var('y'), Var('z'), Var('n'), Var('i'), Var('j'))
(a, b, f, fac, even, odd, foo) = (Var('a'), Var('b'), Var('f'), Var('fac'), Var('even'), Var('odd'), Var('foo'))

def xxxcleanup_vars():
    for v in [k, x, y, z, n, a, b, f, fac, even, odd, foo]:
        v.binding = None

    return