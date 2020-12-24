# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLPrimitiveResidueClass.py
# Compiled at: 2018-04-23 08:51:10
from .NTLCoprimalityTest import coprimalityTest
from .NTLUtilities import jsrange
from .NTLValidations import int_check, pos_check
__all__ = [
 'primitiveResidueClass']
nickname = 'prc'

def primitiveResidueClass(n):
    int_check(n)
    pos_check(n)
    rst = []
    for d in jsrange(1, n):
        if coprimalityTest(d, n) == 1:
            rst.append(d)

    return rst