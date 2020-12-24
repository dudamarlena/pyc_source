# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6019.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5652
MAX = float('inf')

class BinaryTime(univ.Integer):
    __module__ = __name__


BinaryTime.subtypeSpec = constraint.ValueRangeConstraint(0, MAX)
id_aa_binarySigningTime = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.46')

class BinarySigningTime(BinaryTime):
    __module__ = __name__


_cmsAttributesMapUpdate = {id_aa_binarySigningTime: BinarySigningTime()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)