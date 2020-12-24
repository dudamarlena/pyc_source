# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLPrimeFactorisation.py
# Compiled at: 2018-04-23 08:51:10
from .NTLEratosthenesSieve import eratosthenesSieve
from .NTLExceptions import KeywordError
from .NTLUtilities import jsrange
from .NTLValidations import int_check, bool_check, pos_check
__all__ = [
 'primeFactorisation', 'EDLoop', 'wrap']
nickname = 'factor'

def primeFactorisation(N, **kwargs):
    int_check(N)
    p = []
    if N < 0:
        p.append(-1)
        N = -N
    prmList = eratosthenesSieve(N + 1)
    for kw in kwargs:
        if kw != 'wrap':
            raise KeywordError("Keyword '%s' is not defined." % kw)
        else:
            bool_check(kwargs[kw])
            if kwargs[kw]:
                q = [1] if p == [-1] else []
                if N == 0:
                    p.append(0)
                    q.append(1)
                    return (p, q)
                if N == 1:
                    p.append(1)
                    q.append(1)
                    return (p, q)
                return wrap(EDLoop(N, prmList, p))

    if N == 0:
        p.append(0)
        return p
    if N == 1:
        p.append(1)
        return p
    return EDLoop(N, prmList, p)


def EDLoop(N, prmList, rst):
    if N == 1:
        return rst
    for prm in prmList:
        if N % prm == 0:
            rst.append(prm)
            N //= prm
            break

    return EDLoop(N, prmList, rst)


def wrap(table):
    p = []
    q = []
    ctr = 1
    for i in jsrange(1, len(table)):
        if table[i] == table[(i - 1)]:
            ctr += 1
        else:
            p.append(table[(i - 1)])
            q.append(ctr)
            ctr = 1
        if i == len(table) - 1:
            p.append(table[i])
            q.append(ctr)

    if len(table) == 1:
        p.append(table[(-1)])
        q.append(1)
    return (p, q)