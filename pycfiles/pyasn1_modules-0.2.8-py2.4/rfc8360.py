# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8360.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
from pyasn1_modules import rfc3779
from pyasn1_modules import rfc5280
id_pe_ipAddrBlocks_v2 = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.28')
IPAddrBlocks = rfc3779.IPAddrBlocks
id_pe_autonomousSysIds_v2 = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.29')
ASIdentifiers = rfc3779.ASIdentifiers
_certificateExtensionsMapUpdate = {id_pe_ipAddrBlocks_v2: IPAddrBlocks(), id_pe_autonomousSysIds_v2: ASIdentifiers()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)