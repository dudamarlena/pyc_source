# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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