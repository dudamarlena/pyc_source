# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/rfc1157.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ, tag, namedtype, namedval
from pysnmp.proto import rfc1155
__all__ = [
 'GetNextRequestPDU', 'GetResponsePDU', 'SetRequestPDU', 'TrapPDU', 'GetRequestPDU']

class VarBind(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('name', rfc1155.ObjectName()), namedtype.NamedType('value', rfc1155.ObjectSyntax()))


class VarBindList(univ.SequenceOf):
    __module__ = __name__
    componentType = VarBind()


errorStatus = univ.Integer(namedValues=namedval.NamedValues(('noError', 0), ('tooBig',
                                                                             1), ('noSuchName',
                                                                                  2), ('badValue',
                                                                                       3), ('readOnly',
                                                                                            4), ('genErr',
                                                                                                 5)))

class _RequestBase(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('request-id', univ.Integer()), namedtype.NamedType('error-status', errorStatus), namedtype.NamedType('error-index', univ.Integer()), namedtype.NamedType('variable-bindings', VarBindList()))


class GetRequestPDU(_RequestBase):
    __module__ = __name__
    tagSet = _RequestBase.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))


class GetNextRequestPDU(_RequestBase):
    __module__ = __name__
    tagSet = _RequestBase.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))


class GetResponsePDU(_RequestBase):
    __module__ = __name__
    tagSet = _RequestBase.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))


class SetRequestPDU(_RequestBase):
    __module__ = __name__
    tagSet = _RequestBase.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))


genericTrap = univ.Integer().clone(namedValues=namedval.NamedValues(('coldStart', 0), ('warmStart',
                                                                                       1), ('linkDown',
                                                                                            2), ('linkUp',
                                                                                                 3), ('authenticationFailure',
                                                                                                      4), ('egpNeighborLoss',
                                                                                                           5), ('enterpriseSpecific',
                                                                                                                6)))

class TrapPDU(univ.Sequence):
    __module__ = __name__
    tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))
    componentType = namedtype.NamedTypes(namedtype.NamedType('enterprise', univ.ObjectIdentifier()), namedtype.NamedType('agent-addr', rfc1155.NetworkAddress()), namedtype.NamedType('generic-trap', genericTrap), namedtype.NamedType('specific-trap', univ.Integer()), namedtype.NamedType('time-stamp', rfc1155.TimeTicks()), namedtype.NamedType('variable-bindings', VarBindList()))


class PDUs(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('get-request', GetRequestPDU()), namedtype.NamedType('get-next-request', GetNextRequestPDU()), namedtype.NamedType('get-response', GetResponsePDU()), namedtype.NamedType('set-request', SetRequestPDU()), namedtype.NamedType('trap', TrapPDU()))


version = univ.Integer(namedValues=namedval.NamedValues(('version-1', 0)))

class Message(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', version), namedtype.NamedType('community', univ.OctetString()), namedtype.NamedType('data', PDUs()))