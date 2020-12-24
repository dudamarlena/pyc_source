# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/api/verdec.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ
from pyasn1.codec.ber import decoder, eoo
from pyasn1.error import PyAsn1Error
from pysnmp.proto.error import ProtocolError

def decodeMessageVersion(wholeMsg):
    try:
        (seq, wholeMsg) = decoder.decode(wholeMsg, asn1Spec=univ.Sequence(), recursiveFlag=False, substrateFun=lambda a, b, c: (
         a, b[:c]))
        (ver, wholeMsg) = decoder.decode(wholeMsg, asn1Spec=univ.Integer(), recursiveFlag=False, substrateFun=lambda a, b, c: (
         a, b[:c]))
        if eoo.endOfOctets.isSameTypeWith(ver):
            raise ProtocolError('EOO at SNMP version component')
        return ver
    except PyAsn1Error:
        raise ProtocolError('Invalid BER at SNMP version component')