# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc4334.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
id_pe = univ.ObjectIdentifier('1.3.6.1.5.5.7.1')
id_kp = univ.ObjectIdentifier('1.3.6.1.5.5.7.3')
id_aca = univ.ObjectIdentifier('1.3.6.1.5.5.7.10')
id_kp_eapOverPPP = id_kp + (13, )
id_kp_eapOverLAN = id_kp + (14, )
id_pe_wlanSSID = id_pe + (13, )

class SSID(univ.OctetString):
    __module__ = __name__
    constraint.ValueSizeConstraint(1, 32)


class SSIDList(univ.SequenceOf):
    __module__ = __name__
    componentType = SSID()
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


id_aca_wlanSSID = id_aca + (7, )
_certificateExtensionsMap = {id_pe_wlanSSID: SSIDList()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMap)
_certificateAttributesMapUpdate = {id_aca_wlanSSID: SSIDList()}
rfc5280.certificateAttributesMap.update(_certificateAttributesMapUpdate)