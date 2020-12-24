# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/ntl.py
# Compiled at: 2018-04-23 08:51:10
__doc__ = '\nAlternative declaration:\n__import__([folder.]module).[module.]function(*args, **kwargs)\n'
from .NTLArchive import NTLCongruence
from .NTLArchive import NTLFraction
from .NTLArchive import NTLIndex
from .NTLArchive import NTLJacobi
from .NTLArchive import NTLLegendre
from .NTLArchive import NTLPolynomial
from .NTLArchive import NTLQuadratic
__all__ = [
 'Congruence', 'Fraction', 'Index', 'Jacobi', 'Legendre', 'Polynomial', 'Quadratic',
 'bezout', 'binary', 'carmicheal', 'congsolve', 'coprime', 'crt', 'decomposit',
 'eealist', 'euler', 'factor', 'fraction', 'gcd', 'isdivisible', 'isprime',
 'jacobi', 'lcm', 'legendre', 'modulo', 'ord', 'polydiv', 'prc', 'prime', 'primelist',
 'pseudo', 'quadratic', 'root', 'simplify']

class Congruence(NTLCongruence.Congruence):
    pass


class Fraction(NTLFraction.Fraction):
    pass


class Index(NTLIndex.Index):
    pass


class Jacobi(NTLJacobi.Jacobi):
    pass


class Legendre(NTLLegendre.Legendre):
    pass


class Polynomial(NTLPolynomial.Polynomial):
    pass


class Quadratic(NTLQuadratic.Quadratic):
    pass


def bezout(a, b):
    from .NTLArchive import NTLBezoutEquation
    return NTLBezoutEquation.bezoutEquation(a, b)


def binary(a, b, c):
    from .NTLArchive import NTLBinaryEquation
    return NTLBinaryEquation.binaryEquation(a, b, c)


def carmicheal(N):
    from .NTLArchive import NTLCarmichealTest
    return NTLCarmichealTest.carmichealTest(N)


def congsolve(cgcExp, cgcCoe, modulo, **kwargs):
    from .NTLArchive import NTLPolynomialCongruence
    return NTLPolynomialCongruence.polynomialCongruence(cgcExp, cgcCoe, modulo, **kwargs)


def coprime(a, b):
    from .NTLArchive import NTLCoprimalityTest
    return NTLCoprimalityTest.coprimalityTest(a, b)


def crt(*args):
    from .NTLArchive import NTLChineseRemainderTheorem
    return NTLChineseRemainderTheorem.CHNRemainderTheorem(*args)


def decomposit(N, **kwargs):
    from .NTLArchive import NTLQuadraticFactorisation
    return NTLQuadraticFactorisation.quadraticFactorisation(N, **kwargs)


def eealist(a, b):
    from .NTLArchive import NTLEuclideanAlgorithm
    return NTLEuclideanAlgorithm.euclideanAlgorithm(a, b)


def euler(m):
    from .NTLArchive import NTLEulerFunction
    return NTLEulerFunction.eulerFunction(m)


def factor(N, **kwargs):
    from .NTLArchive import NTLPrimeFactorisation
    return NTLPrimeFactorisation.primeFactorisation(N, **kwargs)


def fraction(n, d=None):
    from .NTLArchive import NTLContinuedFraction
    return NTLContinuedFraction.continuedFraction(n, d)


def gcd(a, b):
    from .NTLArchive import NTLGreatestCommonDivisor
    return NTLGreatestCommonDivisor.greatestCommonDivisor(a, b)


def isdivisible(a, b):
    from .NTLArchive import NTLEuclideanDivision
    return NTLEuclideanDivision.euclideanDivision(a, b)


def isprime(N):
    from .NTLArchive import NTLTrivialDivision
    return NTLTrivialDivision.trivialDivision(N)


def jacobi(a, m):
    from .NTLArchive import NTLJacobiSymbol
    return NTLJacobiSymbol.jacobiSymbol(a, m)


def lcm(a, b):
    from .NTLArchive import NTLLeastCommonMultiple
    return NTLLeastCommonMultiple.leastCommonMultiple(a, b)


def legendre(a, p, **kwargs):
    from .NTLArchive import NTLLegendreSymbol
    return NTLLegendreSymbol.legendreSymbol(a, p, **kwargs)


def modulo(b, e, m):
    from .NTLArchive import NTLRepetiveSquareModulo
    return NTLRepetiveSquareModulo.repetiveSquareModulo(b, e, m)


def ord(m, a):
    from .NTLArchive import NTLOrder
    return NTLOrder.order(m, a)


def polydiv(dvdExp, dvdCoe, dvsExp, dvsCoe):
    from .NTLArchive import NTLPolynomialEuclideanDivision
    return NTLPolynomialEuclideanDivision.polyED(dvdExp, dvdCoe, dvsExp, dvsCoe)


def prc(m):
    from .NTLArchive import NTLPrimitiveResidueClass
    return NTLPrimitiveResidueClass.primitiveResidueClass(m)


def prime(upper, lower=None, steps=None):
    from .NTLArchive import NTLEratosthenesSieve
    return NTLEratosthenesSieve.primerange(upper, lower, steps)


def primelist(upper, lower=None):
    from .NTLArchive import NTLEratosthenesSieve
    return NTLEratosthenesSieve.eratosthenesSieve(upper, lower)


def pseudo(**kwargs):
    from .NTLArchive import NTLPseudoPrime
    return NTLPseudoPrime.pseudoPrime(**kwargs)


def quadratic(p, **kwargs):
    from .NTLArchive import NTLQuadraticEquation
    return NTLQuadraticEquation.quadraticEquation(p, **kwargs)


def root(m):
    from .NTLArchive import NTLPrimitiveRoot
    return NTLPrimitiveRoot.primitiveRoot(m)


def simplify(cgcExp, cgcCoe, modulo, **kwargs):
    from .NTLArchive import NTLCongruenceSimplification
    return NTLCongruenceSimplification.congruenceSimplification(cgcExp, cgcCoe, modulo, **kwargs)