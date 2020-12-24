# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLRepetiveSquareModulo.py
# Compiled at: 2018-04-23 08:51:10
from .NTLValidations import int_check, notneg_check, pos_check
__all__ = [
 'repetiveSquareModulo']
nickname = 'modulo'

def repetiveSquareModulo(base, exponent, modulo):
    int_check(base, exponent, modulo)
    pos_check(modulo)
    notneg_check(exponent)
    if base == 0:
        if exponent != 0:
            return 0
        return 1
    if exponent == 0:
        return 1
    get_bin = lambda x: format(x, 'b')
    exp_bin = get_bin(exponent)
    ptr = len(exp_bin) - 1
    a = 1
    b = base
    n = exp_bin
    while ptr >= 0:
        a = a * b ** int(n[ptr]) % modulo
        b = b ** 2 % modulo
        ptr -= 1

    if base > 0:
        return a
    return -1 * a