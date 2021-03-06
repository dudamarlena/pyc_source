# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLCoprimalityTest.py
# Compiled at: 2018-04-23 08:51:10
from .NTLGreatestCommonDivisor import greatestCommonDivisor
from .NTLValidations import int_check
__all__ = [
 'coprimalityTest']
nickname = 'coprime'

def coprimalityTest(a, b):
    int_check(a, b)
    if greatestCommonDivisor(a, b) == 1:
        return True
    return False