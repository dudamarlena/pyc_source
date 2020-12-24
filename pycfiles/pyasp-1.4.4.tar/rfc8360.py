# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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