# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc1157.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc1155

class Version(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('version-1', 0))
    defaultValue = 0


class Community(univ.OctetString):
    __module__ = __name__


class RequestID(univ.Integer):
    __module__ = __name__


class ErrorStatus(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('noError', 0), ('tooBig', 1), ('noSuchName',
                                                                       2), ('badValue',
                                                                            3), ('readOnly',
                                                                                 4), ('genErr',
                                                                                      5))


class ErrorIndex(univ.Integer):
    __module__ = __name__


class VarBind(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('name', rfc1155.ObjectName()), namedtype.NamedType('value', rfc1155.ObjectSyntax()))


class VarBindList(univ.SequenceOf):
    __module__ = __name__
    componentType = VarBind()


class _RequestBase(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('request-id', RequestID()), namedtype.NamedType('error-status', ErrorStatus()), namedtype.NamedType('error-index', ErrorIndex()), namedtype.NamedType('variable-bindings', VarBindList()))


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


class TrapPDU(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('enterprise', univ.ObjectIdentifier()), namedtype.NamedType('agent-addr', rfc1155.NetworkAddress()), namedtype.NamedType('generic-trap', univ.Integer().clone(namedValues=namedval.NamedValues(('coldStart',
                                                                                                                                                                                                                                                             0), ('warmStart',
                                                                                                                                                                                                                                                                  1), ('linkDown',
                                                                                                                                                                                                                                                                       2), ('linkUp',
                                                                                                                                                                                                                                                                            3), ('authenticationFailure',
                                                                                                                                                                                                                                                                                 4), ('egpNeighborLoss',
                                                                                                                                                                                                                                                                                      5), ('enterpriseSpecific',
                                                                                                                                                                                                                                                                                           6)))), namedtype.NamedType('specific-trap', univ.Integer()), namedtype.NamedType('time-stamp', rfc1155.TimeTicks()), namedtype.NamedType('variable-bindings', VarBindList()))


class Pdus(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('get-request', GetRequestPDU()), namedtype.NamedType('get-next-request', GetNextRequestPDU()), namedtype.NamedType('get-response', GetResponsePDU()), namedtype.NamedType('set-request', SetRequestPDU()), namedtype.NamedType('trap', TrapPDU()))


class Message(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('community', Community()), namedtype.NamedType('data', Pdus()))