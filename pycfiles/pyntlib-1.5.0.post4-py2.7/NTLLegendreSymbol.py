# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLLegendreSymbol.py
# Compiled at: 2018-04-23 08:51:10
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLValidations import bool_check, int_check, prime_check
__all__ = [
 'legendreSymbol']
nickname = 'legendre'

def legendreSymbol(a, p, **kwargs):
    trust = False
    for kw in kwargs:
        if kw != 'trust':
            raise KeywordError("Keyword '%s' is not defined." % kw)
        else:
            trust = kwargs[kw]
            bool_check(trust)

    int_check(a)
    prime_check(trust, p)
    a %= p
    if a == 1:
        return 1
    if a == p - 1:
        return (-1) ** ((p - 1) // 2)
    if a == 2:
        return (-1) ** ((p ** 2 - 1) // 8)
    mod = repetiveSquareModulo(a, (p - 1) // 2, p)
    if mod != p - 1:
        return mod
    return -1