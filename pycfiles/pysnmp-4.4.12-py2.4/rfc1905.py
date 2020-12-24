# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/rfc1905.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ, tag, constraint, namedtype, namedval
from pysnmp.proto import rfc1902
__all__ = [
 'unSpecified', 'EndOfMibView', 'ReportPDU', 'UnSpecified', 'BulkPDU', 'SNMPv2TrapPDU', 'GetRequestPDU', 'NoSuchObject', 'GetNextRequestPDU', 'GetBulkRequestPDU', 'NoSuchInstance', 'ResponsePDU', 'noSuchObject', 'InformRequestPDU', 'endOfMibView', 'SetRequestPDU', 'noSuchInstance']
max_bindings = rfc1902.Integer(2147483647)
UnSpecified = univ.Null
unSpecified = UnSpecified('')

class NoSuchObject(univ.Null):
    __module__ = __name__
    tagSet = univ.Null.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))

    def prettyPrint(self, scope=0):
        return 'No Such Object currently exists at this OID'


noSuchObject = NoSuchObject('')

class NoSuchInstance(univ.Null):
    __module__ = __name__
    tagSet = univ.Null.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))

    def prettyPrint(self, scope=0):
        return 'No Such Instance currently exists at this OID'


noSuchInstance = NoSuchInstance('')

class EndOfMibView(univ.Null):
    __module__ = __name__
    tagSet = univ.Null.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))

    def prettyPrint(self, scope=0):
        return 'No more variables left in this MIB View'


endOfMibView = EndOfMibView('')

class _BindValue(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('value', rfc1902.ObjectSyntax()), namedtype.NamedType('unSpecified', unSpecified), namedtype.NamedType('noSuchObject', noSuchObject), namedtype.NamedType('noSuchInstance', noSuchInstance), namedtype.NamedType('endOfMibView', endOfMibView))


class VarBind(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('name', rfc1902.ObjectName()), namedtype.NamedType('', _BindValue()))


class VarBindList(univ.SequenceOf):
    __module__ = __name__
    componentType = VarBind()
    subtypeSpec = univ.SequenceOf.subtypeSpec + constraint.ValueSizeConstraint(0, max_bindings)


errorStatus = univ.Integer(namedValues=namedval.NamedValues(('noError', 0), ('tooBig',
                                                                             1), ('noSuchName',
                                                                                  2), ('badValue',
                                                                                       3), ('readOnly',
                                                                                            4), ('genErr',
                                                                                                 5), ('noAccess',
                                                                                                      6), ('wrongType',
                                                                                                           7), ('wrongLength',
                                                                                                                8), ('wrongEncoding',
                                                                                                                     9), ('wrongValue',
                                                                                                                          10), ('noCreation',
                                                                                                                                11), ('inconsistentValue',
                                                                                                                                      12), ('resourceUnavailable',
                                                                                                                                            13), ('commitFailed',
                                                                                                                                                  14), ('undoFailed',
                                                                                                                                                        15), ('authorizationError',
                                                                                                                                                              16), ('notWritable',
                                                                                                                                                                    17), ('inconsistentName',
                                                                                                                                                                          18)))

class PDU(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('request-id', rfc1902.Integer32()), namedtype.NamedType('error-status', errorStatus), namedtype.NamedType('error-index', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, max_bindings))), namedtype.NamedType('variable-bindings', VarBindList()))


nonRepeaters = univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, max_bindings))
maxRepetitions = univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, max_bindings))

class BulkPDU(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('request-id', rfc1902.Integer32()), namedtype.NamedType('non-repeaters', nonRepeaters), namedtype.NamedType('max-repetitions', maxRepetitions), namedtype.NamedType('variable-bindings', VarBindList()))


class GetRequestPDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))


class GetNextRequestPDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))


class ResponsePDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))


class SetRequestPDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))


class GetBulkRequestPDU(BulkPDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5))


class InformRequestPDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6))


class SNMPv2TrapPDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 7))


class ReportPDU(PDU):
    __module__ = __name__
    tagSet = PDU.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 8))


class PDUs(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('get-request', GetRequestPDU()), namedtype.NamedType('get-next-request', GetNextRequestPDU()), namedtype.NamedType('get-bulk-request', GetBulkRequestPDU()), namedtype.NamedType('response', ResponsePDU()), namedtype.NamedType('set-request', SetRequestPDU()), namedtype.NamedType('inform-request', InformRequestPDU()), namedtype.NamedType('snmpV2-trap', SNMPv2TrapPDU()), namedtype.NamedType('report', ReportPDU()))