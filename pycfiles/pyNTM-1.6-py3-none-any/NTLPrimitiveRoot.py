# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLPrimitiveRoot.py
# Compiled at: 2018-04-23 08:51:10
from .NTLCoprimalityTest import coprimalityTest
from .NTLEulerFunction import eulerFunction
from .NTLExceptions import SolutionError
from .NTLGreatestCommonDivisor import greatestCommonDivisor
from .NTLPrimeFactorisation import primeFactorisation
from .NTLPrimitiveResidueClass import primitiveResidueClass
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLUtilities import jsrange
from .NTLValidations import int_check, pos_check
__all__ = [
 'primitiveRoot',
 'primePR', 'exponentPR', 'binaryPR']
nickname = 'root'

def primitiveRoot(m):
    int_check(m)
    pos_check(m)
    if m == 2:
        return [1]
    if m == 4:
        return [3]
    p, q = primeFactorisation(m, wrap=True)
    if len(p) == 1:
        if q[0] == 1:
            return primePR(p[0])
        return exponentPR(p[0], q[0])
    if len(p) == 2 and q[0] == 1:
        return binaryPR(p[1], q[1])
    raise SolutionError('%d has no primitive root.' % m)


def primePR(prime):
    primitiveRoot = []
    q = primeFactorisation(prime - 1, wrap=True)[0]
    for g in jsrange(1, prime):
        for qitem in q:
            exp = (prime - 1) // qitem
            if repetiveSquareModulo(g, exp, prime) == 1:
                break
        else:
            break

    prc = primitiveResidueClass(prime - 1)
    for num in prc:
        primitiveRoot.append(repetiveSquareModulo(g, num, prime))

    return sorted(primitiveRoot)


def exponentPR(base, exponent):
    primitiveRoot = []
    prrList = primePR(base)
    for prr in prrList:
        if prr ** (base - 1) % base == 1 and greatestCommonDivisor(base, prr ** (base - 1) // base) == 1:
            g = prr
            break
        if (prr + base) ** (base - 1) % base == 1 and greatestCommonDivisor(base, (prr + base) ** (base - 1) // base) == 1:
            g = prr + base
            break

    prc = primitiveResidueClass(eulerFunction(base ** 2))
    for num in prc:
        primitiveRoot.append(repetiveSquareModulo(g, num, base ** exponent))

    return sorted(primitiveRoot)


def binaryPR(base, exponent):
    primitiveRoot = []
    glist = exponentPR(base, exponent)
    for g in glist:
        if g % 2 == 1:
            primitiveRoot.append(g)
        g_ = g + base ** exponent
        if g_ % 2 == 1:
            primitiveRoot.append(g_)

    return sorted(primitiveRoot)