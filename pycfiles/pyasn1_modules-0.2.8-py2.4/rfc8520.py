# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8520.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import char
from pyasn1.type import univ
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
id_pe_mud_url = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.25')

class MUDURLSyntax(char.IA5String):
    __module__ = __name__


id_pe_mudsigner = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.30')

class MUDsignerSyntax(rfc5280.Name):
    __module__ = __name__


id_ct_mudtype = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.41')
_certificateExtensionsMapUpdate = {id_pe_mud_url: MUDURLSyntax(), id_pe_mudsigner: MUDsignerSyntax()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
_cmsContentTypesMapUpdate = {id_ct_mudtype: univ.OctetString()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)