# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLTrivialDivision.py
# Compiled at: 2018-04-23 08:51:10
import math
from .NTLEratosthenesSieve import eratosthenesSieve
from .NTLExceptions import DefinitionError
from .NTLUtilities import jsfloor, jsmaxint, jsrange
from .NTLValidations import int_check, pos_check
__all__ = [
 'trivialDivision']
nickname = 'isprime'

def trivialDivision(N):
    int_check(N)
    pos_check(N)
    if N == 1 or N == 0:
        raise DefinitionError('The argument must be a natural number greater than 1.')
    if math.log(N, 10) <= 7.0:
        table = eratosthenesSieve(N + 1)
        if N in table:
            return True
        return False
    try:
        byte = math.log(N, 2) - 1
        para = 3 ** jsfloor(math.log(2 ** byte, 10) // 3)
    except (OverflowError, MemoryError):
        para = jsmaxint

    from .NTLPseudoPrime import miller_rabinTest
    if miller_rabinTest(N, para):
        return True
    else:
        return False