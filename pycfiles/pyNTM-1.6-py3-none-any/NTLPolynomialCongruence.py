# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLPolynomialCongruence.py
# Compiled at: 2018-04-23 08:51:10
from .NTLChineseRemainderTheorem import CHNRemainderTheorem
from .NTLCongruenceSimplification import congruenceSimplification
from .NTLExceptions import SolutionError
from .NTLGreatestCommonDivisor import greatestCommonDivisor
from .NTLPrimeFactorisation import primeFactorisation
from .NTLRepetiveSquareModulo import repetiveSquareModulo
from .NTLTrivialDivision import trivialDivision
from .NTLUtilities import jsrange
from .NTLValidations import int_check, list_check, pos_check
__all__ = [
 'polynomialCongruence',
 'prmMCS', 'cpsMCS',
 'prmMCSLite', 'prmMCSPro',
 'makePolynomial', 'polyDerivative']
nickname = 'congsolve'

def polynomialCongruence(cgcExp, cgcCoe, modulo, **kwargs):
    list_check(cgcExp, cgcCoe)
    int_check(modulo)
    pos_check(modulo)
    trust = False
    for kw in kwargs:
        if kw != 'trust':
            raise KeywordError("Keyword '%s' is not defined." % kw)
        else:
            trust = kwargs[kw]
            bool_check(trust)

    if trust or trivialDivision(modulo):
        remainder = prmMCS(cgcExp, cgcCoe, modulo)
    else:
        remainder = cpsMCS(cgcExp, cgcCoe, modulo)
    if len(remainder) == 0:
        raise SolutionError('The polynomial congruence has no integral solution.')
    return sorted(remainder)


def prmMCS(cgcExp, cgcCoe, modulo):
    remainder = []
    rmdExp, rmdCoe = congruenceSimplification(cgcExp, cgcCoe, modulo)
    polyCgc = makePolynomial(rmdExp, rmdCoe)
    r = lambda x: eval(polyCgc)
    for x in jsrange(modulo):
        if r(x) % modulo == 0:
            remainder.append(x)

    return remainder


def makePolynomial(expList, coeList):
    polynomial = ''
    for ptr in jsrange(len(expList)):
        polynomial += str(coeList[ptr]) + '*x**' + str(expList[ptr])
        if ptr < len(expList) - 1:
            polynomial += ' + '

    return polynomial


def cpsMCS(cgcExp, cgcCoe, modulo):
    p, q = primeFactorisation(modulo, wrap=True)
    if len(p) == 1:
        tmpMod = p[0]
        tmpExp = q[0]
        remainder = prmMCSLite(cgcExp, cgcCoe, tmpMod, tmpExp)
    else:
        tmpRmd = []
        tmpMod = []
        for ptr in jsrange(len(p)):
            tmpModVar = p[ptr]
            tmpExpVar = q[ptr]
            tmpMod.append(tmpModVar ** tmpExpVar)
            tmpRmd.append(prmMCSLite(cgcExp, cgcCoe, tmpModVar, tmpExpVar))

        remainder = CHNRemainderTheorem(*zip(tmpMod, tmpRmd))
    return remainder


def prmMCSLite(cgcExp, cgcCoe, mod, exp):
    tmpRmd = prmMCS(cgcExp, cgcCoe, mod)
    if exp == 1:
        return tmpRmd
    remainder = prmMCSPro(cgcExp, cgcCoe, tmpRmd, mod, exp)
    return remainder


def prmMCSPro(cgcExp, cgcCoe, rmd, mod, exp):
    drvExp, drvCoe = polyDerivative(cgcExp, cgcCoe)
    polyDrv = makePolynomial(drvExp, drvCoe)
    drv = lambda x: eval(polyDrv)
    for tmpRmd in rmd:
        if greatestCommonDivisor(drv(tmpRmd), mod) == 1:
            polyDrvMod = 0
            for ptr in jsrange(len(drvExp)):
                polyDrvMod += repetiveSquareModulo(drvCoe[ptr] * tmpRmd, drvExp[ptr], mod)

            x = tmpRmd
            polyDrvMod = polyDrvMod % mod - mod
            polyDrvRcp = 1 / polyDrvMod
            break

    for ctr in jsrange(0, exp):
        poly = makePolynomial(cgcExp, cgcCoe)
        fx = lambda x: eval(poly)
        t = -1 * fx(x) / mod ** ctr * polyDrvRcp % mod
        x += t * mod ** ctr % mod ** (ctr + 1)

    return [
     x]


def polyDerivative(cgcExp, cgcCoe):
    drvExp = []
    drvCoe = []
    for ptr in jsrange(len(cgcExp)):
        if cgcExp[ptr] != 0:
            drvExp.append(cgcExp[ptr] - 1)
            drvCoe.append(cgcCoe[ptr] * cgcExp[ptr])

    return (drvExp, drvCoe)