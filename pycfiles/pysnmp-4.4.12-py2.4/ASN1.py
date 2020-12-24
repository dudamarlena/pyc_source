# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/ASN1.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ
from pysnmp.proto import rfc1902
mibBuilder.exportSymbols('ASN1', ObjectIdentifier=univ.ObjectIdentifier, Integer=rfc1902.Integer32, OctetString=rfc1902.OctetString)