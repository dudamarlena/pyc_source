# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5940.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc2560
from pyasn1_modules import rfc5652
id_ri_ocsp_response = univ.ObjectIdentifier('1.3.6.1.5.5.7.16.2')
OCSPResponse = rfc2560.OCSPResponse
id_ri_scvp = univ.ObjectIdentifier('1.3.6.1.5.5.7.16.4')
ContentInfo = rfc5652.ContentInfo

class SCVPReqRes(univ.Sequence):
    __module__ = __name__


SCVPReqRes.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('request', ContentInfo().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('response', ContentInfo()))
_otherRevInfoFormatMapUpdate = {id_ri_ocsp_response: OCSPResponse(), id_ri_scvp: SCVPReqRes()}
rfc5652.otherRevInfoFormatMap.update(_otherRevInfoFormatMapUpdate)