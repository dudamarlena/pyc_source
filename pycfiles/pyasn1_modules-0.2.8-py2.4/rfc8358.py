# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8358.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
from pyasn1_modules import rfc5652
id_ct = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1')
id_ct_asciiTextWithCRLF = id_ct + (27, )
id_ct_epub = id_ct + (39, )
id_ct_htmlWithCRLF = id_ct + (38, )
id_ct_pdf = id_ct + (29, )
id_ct_postscript = id_ct + (30, )
id_ct_utf8TextWithCRLF = id_ct + (37, )
id_ct_xml = id_ct + (28, )
_cmsContentTypesMapUpdate = {id_ct_asciiTextWithCRLF: univ.OctetString(), id_ct_epub: univ.OctetString(), id_ct_htmlWithCRLF: univ.OctetString(), id_ct_pdf: univ.OctetString(), id_ct_postscript: univ.OctetString(), id_ct_utf8TextWithCRLF: univ.OctetString(), id_ct_xml: univ.OctetString()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)