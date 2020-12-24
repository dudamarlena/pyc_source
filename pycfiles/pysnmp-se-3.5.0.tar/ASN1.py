# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/ASN1.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ
from pysnmp.proto import rfc1902
mibBuilder.exportSymbols('ASN1', ObjectIdentifier=univ.ObjectIdentifier, Integer=rfc1902.Integer32, OctetString=rfc1902.OctetString)