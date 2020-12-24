# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLEuclideanAlgorithm.py
# Compiled at: 2018-04-23 08:51:10
from .NTLExceptions import DefinitionError
from .NTLPolynomial import Polynomial
from .NTLValidations import int_check
__all__ = [
 'euclideanAlgorithm', 'EEALoop']
nickname = 'eealist'

def euclideanAlgorithm(dividend, divisor):
    if isinstance(dividend, Polynomial) or isinstance(divisor, Polynomial):
        dividend = Polynomial(dividend)
        divisor = Polynomial(divisor)
    else:
        int_check(dividend, divisor)
        if divisor == 0:
            raise DefinitionError('The divisor should never be zero.')
    return EEALoop(dividend, divisor, [])


def EEALoop(a, b, qSet):
    q, r = divmod(a, b)
    if r == 0:
        return qSet
    else:
        qSet.append(q)
        return EEALoop(b, r, qSet)