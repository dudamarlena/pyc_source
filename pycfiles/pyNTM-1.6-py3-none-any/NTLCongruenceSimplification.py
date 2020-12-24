# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLCongruenceSimplification.py
# Compiled at: 2018-04-23 08:51:10
from .NTLExceptions import KeywordError
from .NTLPolynomialEuclideanDivision import polyED
from .NTLValidations import bool_check, list_check, prime_check
__all__ = [
 'congruenceSimplification']
nickname = 'simplify'

def congruenceSimplification(cgcExp, cgcCoe, modulo, **kwargs):
    trust = False
    for kw in kwargs:
        if kw != 'trust':
            raise KeywordError("Keyword '%s' is not defined." % kw)
        else:
            trust = kwargs[kw]
            bool_check(trust)

    list_check(cgcExp, cgcCoe)
    prime_check(trust, modulo)
    dvsExp = [modulo, 1]
    dvsCoe = [1, -1]
    qttExp, qttCoe, rtoExp, rtoCoe = polyED(cgcExp, cgcCoe, dvsExp, dvsCoe)
    return (
     rtoExp, rtoCoe)