# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5913.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5755
MAX = float('inf')
id_pe_clearanceConstraints = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.21')
id_pe_authorityClearanceConstraints = id_pe_clearanceConstraints

class AuthorityClearanceConstraints(univ.SequenceOf):
    __module__ = __name__
    componentType = rfc5755.Clearance()
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


_certificateExtensionsMapUpdate = {id_pe_clearanceConstraints: AuthorityClearanceConstraints()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)