# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5916.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_deviceOwner = univ.ObjectIdentifier((2, 16, 840, 1, 101, 2, 1, 5, 69))
at_deviceOwner = rfc5280.Attribute()
at_deviceOwner['type'] = id_deviceOwner
at_deviceOwner['values'][0] = univ.ObjectIdentifier()
_certificateAttributesMapUpdate = {id_deviceOwner: univ.ObjectIdentifier()}
rfc5280.certificateAttributesMap.update(_certificateAttributesMapUpdate)