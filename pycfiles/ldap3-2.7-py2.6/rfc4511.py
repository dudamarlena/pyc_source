# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\rfc4511.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from pyasn1.type.univ import OctetString, Integer, Sequence, Choice, SequenceOf, Boolean, Null, Enumerated, SetOf
from pyasn1.type.namedtype import NamedTypes, NamedType, OptionalNamedType, DefaultedNamedType
from pyasn1.type.constraint import ValueRangeConstraint, SingleValueConstraint, ValueSizeConstraint
from pyasn1.type.namedval import NamedValues
from pyasn1.type.tag import tagClassApplication, tagFormatConstructed, Tag, tagClassContext, tagFormatSimple
LDAP_MAX_INT = 2147483647
MAXINT = Integer(LDAP_MAX_INT)
rangeInt0ToMaxConstraint = ValueRangeConstraint(0, MAXINT)
rangeInt1To127Constraint = ValueRangeConstraint(1, 127)
size1ToMaxConstraint = ValueSizeConstraint(1, MAXINT)
responseValueConstraint = SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 32, 33, 34, 36, 48, 49, 50, 51, 52, 53, 54, 64, 65, 66, 67, 68, 69, 71, 80, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 4096)
numericOIDConstraint = None
distinguishedNameConstraint = None
nameComponentConstraint = None
attributeDescriptionConstraint = None
uriConstraint = None
attributeSelectorConstraint = None

class Integer0ToMax(Integer):
    subtypeSpec = Integer.subtypeSpec + rangeInt0ToMaxConstraint


class LDAPString(OctetString):
    encoding = 'utf-8'


class MessageID(Integer0ToMax):
    pass


class LDAPOID(OctetString):
    pass


class LDAPDN(LDAPString):
    pass


class RelativeLDAPDN(LDAPString):
    pass


class AttributeDescription(LDAPString):
    pass


class AttributeValue(OctetString):
    encoding = 'utf-8'


class AssertionValue(OctetString):
    encoding = 'utf-8'


class AttributeValueAssertion(Sequence):
    componentType = NamedTypes(NamedType('attributeDesc', AttributeDescription()), NamedType('assertionValue', AssertionValue()))


class MatchingRuleId(LDAPString):
    pass


class Vals(SetOf):
    componentType = AttributeValue()


class ValsAtLeast1(SetOf):
    componentType = AttributeValue()
    subtypeSpec = SetOf.subtypeSpec + size1ToMaxConstraint


class PartialAttribute(Sequence):
    componentType = NamedTypes(NamedType('type', AttributeDescription()), NamedType('vals', Vals()))


class Attribute(Sequence):
    componentType = NamedTypes(NamedType('type', AttributeDescription()), NamedType('vals', Vals()))


class AttributeList(SequenceOf):
    componentType = Attribute()


class Simple(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))
    encoding = 'utf-8'


class Credentials(OctetString):
    encoding = 'utf-8'


class SaslCredentials(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 3))
    componentType = NamedTypes(NamedType('mechanism', LDAPString()), OptionalNamedType('credentials', Credentials()))


class SicilyPackageDiscovery(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 9))
    encoding = 'utf-8'


class SicilyNegotiate(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 10))
    encoding = 'utf-8'


class SicilyResponse(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 11))
    encoding = 'utf-8'


class AuthenticationChoice(Choice):
    componentType = NamedTypes(NamedType('simple', Simple()), NamedType('sasl', SaslCredentials()), NamedType('sicilyPackageDiscovery', SicilyPackageDiscovery()), NamedType('sicilyNegotiate', SicilyNegotiate()), NamedType('sicilyResponse', SicilyResponse()))


class Version(Integer):
    subtypeSpec = Integer.subtypeSpec + rangeInt1To127Constraint


class ResultCode(Enumerated):
    namedValues = NamedValues(('success', 0), ('operationsError', 1), ('protocolError',
                                                                       2), ('timeLimitExceeded',
                                                                            3), ('sizeLimitExceeded',
                                                                                 4), ('compareFalse',
                                                                                      5), ('compareTrue',
                                                                                           6), ('authMethodNotSupported',
                                                                                                7), ('strongerAuthRequired',
                                                                                                     8), ('referral',
                                                                                                          10), ('adminLimitExceeded',
                                                                                                                11), ('unavailableCriticalExtension',
                                                                                                                      12), ('confidentialityRequired',
                                                                                                                            13), ('saslBindInProgress',
                                                                                                                                  14), ('noSuchAttribute',
                                                                                                                                        16), ('undefinedAttributeType',
                                                                                                                                              17), ('inappropriateMatching',
                                                                                                                                                    18), ('constraintViolation',
                                                                                                                                                          19), ('attributeOrValueExists',
                                                                                                                                                                20), ('invalidAttributeSyntax',
                                                                                                                                                                      21), ('noSuchObject',
                                                                                                                                                                            32), ('aliasProblem',
                                                                                                                                                                                  33), ('invalidDNSyntax',
                                                                                                                                                                                        34), ('aliasDereferencingProblem',
                                                                                                                                                                                              36), ('inappropriateAuthentication',
                                                                                                                                                                                                    48), ('invalidCredentials',
                                                                                                                                                                                                          49), ('insufficientAccessRights',
                                                                                                                                                                                                                50), ('busy',
                                                                                                                                                                                                                      51), ('unavailable',
                                                                                                                                                                                                                            52), ('unwillingToPerform',
                                                                                                                                                                                                                                  53), ('loopDetected',
                                                                                                                                                                                                                                        54), ('namingViolation',
                                                                                                                                                                                                                                              64), ('objectClassViolation',
                                                                                                                                                                                                                                                    65), ('notAllowedOnNonLeaf',
                                                                                                                                                                                                                                                          66), ('notAllowedOnRDN',
                                                                                                                                                                                                                                                                67), ('entryAlreadyExists',
                                                                                                                                                                                                                                                                      68), ('objectClassModsProhibited',
                                                                                                                                                                                                                                                                            69), ('affectMultipleDSAs',
                                                                                                                                                                                                                                                                                  71), ('other',
                                                                                                                                                                                                                                                                                        80), ('lcupResourcesExhausted',
                                                                                                                                                                                                                                                                                              113), ('lcupSecurityViolation',
                                                                                                                                                                                                                                                                                                     114), ('lcupInvalidData',
                                                                                                                                                                                                                                                                                                            115), ('lcupUnsupportedScheme',
                                                                                                                                                                                                                                                                                                                   116), ('lcupReloadRequired',
                                                                                                                                                                                                                                                                                                                          117), ('canceled',
                                                                                                                                                                                                                                                                                                                                 118), ('noSuchOperation',
                                                                                                                                                                                                                                                                                                                                        119), ('tooLate',
                                                                                                                                                                                                                                                                                                                                               120), ('cannotCancel',
                                                                                                                                                                                                                                                                                                                                                      121), ('assertionFailed',
                                                                                                                                                                                                                                                                                                                                                             122), ('authorizationDenied',
                                                                                                                                                                                                                                                                                                                                                                    123), ('e-syncRefreshRequired',
                                                                                                                                                                                                                                                                                                                                                                           4096))
    subTypeSpec = Enumerated.subtypeSpec + responseValueConstraint


class URI(LDAPString):
    pass


class Referral(SequenceOf):
    tagSet = SequenceOf.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 3))
    componentType = URI()


class ServerSaslCreds(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 7))
    encoding = 'utf-8'


class LDAPResult(Sequence):
    componentType = NamedTypes(NamedType('resultCode', ResultCode()), NamedType('matchedDN', LDAPDN()), NamedType('diagnosticMessage', LDAPString()), OptionalNamedType('referral', Referral()))


class Criticality(Boolean):
    defaultValue = False


class ControlValue(OctetString):
    encoding = 'utf-8'


class Control(Sequence):
    componentType = NamedTypes(NamedType('controlType', LDAPOID()), DefaultedNamedType('criticality', Criticality()), OptionalNamedType('controlValue', ControlValue()))


class Controls(SequenceOf):
    tagSet = SequenceOf.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 0))
    componentType = Control()


class Scope(Enumerated):
    namedValues = NamedValues(('baseObject', 0), ('singleLevel', 1), ('wholeSubtree',
                                                                      2))


class DerefAliases(Enumerated):
    namedValues = NamedValues(('neverDerefAliases', 0), ('derefInSearching', 1), ('derefFindingBaseObj',
                                                                                  2), ('derefAlways',
                                                                                       3))


class TypesOnly(Boolean):
    pass


class Selector(LDAPString):
    pass


class AttributeSelection(SequenceOf):
    componentType = Selector()


class MatchingRule(MatchingRuleId):
    tagSet = MatchingRuleId.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))


class Type(AttributeDescription):
    tagSet = AttributeDescription.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 2))


class MatchValue(AssertionValue):
    tagSet = AssertionValue.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 3))


class DnAttributes(Boolean):
    tagSet = Boolean.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 4))
    defaultValue = Boolean(False)


class MatchingRuleAssertion(Sequence):
    componentType = NamedTypes(OptionalNamedType('matchingRule', MatchingRule()), OptionalNamedType('type', Type()), NamedType('matchValue', MatchValue()), DefaultedNamedType('dnAttributes', DnAttributes()))


class Initial(AssertionValue):
    tagSet = AssertionValue.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))


class Any(AssertionValue):
    tagSet = AssertionValue.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))


class Final(AssertionValue):
    tagSet = AssertionValue.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 2))


class Substring(Choice):
    componentType = NamedTypes(NamedType('initial', Initial()), NamedType('any', Any()), NamedType('final', Final()))


class Substrings(SequenceOf):
    subtypeSpec = SequenceOf.subtypeSpec + size1ToMaxConstraint
    componentType = Substring()


class SubstringFilter(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 4))
    componentType = NamedTypes(NamedType('type', AttributeDescription()), NamedType('substrings', Substrings()))


class And(SetOf):
    tagSet = SetOf.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 0))
    subtypeSpec = SetOf.subtypeSpec + size1ToMaxConstraint


class Or(SetOf):
    tagSet = SetOf.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 1))
    subtypeSpec = SetOf.subtypeSpec + size1ToMaxConstraint


class Not(Choice):
    pass


class EqualityMatch(AttributeValueAssertion):
    tagSet = AttributeValueAssertion.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 3))


class GreaterOrEqual(AttributeValueAssertion):
    tagSet = AttributeValueAssertion.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 5))


class LessOrEqual(AttributeValueAssertion):
    tagSet = AttributeValueAssertion.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 6))


class Present(AttributeDescription):
    tagSet = AttributeDescription.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 7))


class ApproxMatch(AttributeValueAssertion):
    tagSet = AttributeValueAssertion.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 8))


class ExtensibleMatch(MatchingRuleAssertion):
    tagSet = MatchingRuleAssertion.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatConstructed, 9))


class Filter(Choice):
    componentType = NamedTypes(NamedType('and', And()), NamedType('or', Or()), NamedType('notFilter', Not()), NamedType('equalityMatch', EqualityMatch()), NamedType('substringFilter', SubstringFilter()), NamedType('greaterOrEqual', GreaterOrEqual()), NamedType('lessOrEqual', LessOrEqual()), NamedType('present', Present()), NamedType('approxMatch', ApproxMatch()), NamedType('extensibleMatch', ExtensibleMatch()))


And.componentType = Filter()
Or.componentType = Filter()
Not.componentType = NamedTypes(NamedType('innerNotFilter', Filter()))
Not.tagSet = Filter.tagSet.tagExplicitly(Tag(tagClassContext, tagFormatConstructed, 2))

class PartialAttributeList(SequenceOf):
    componentType = PartialAttribute()


class Operation(Enumerated):
    namedValues = NamedValues(('add', 0), ('delete', 1), ('replace', 2), ('increment',
                                                                          3))


class Change(Sequence):
    componentType = NamedTypes(NamedType('operation', Operation()), NamedType('modification', PartialAttribute()))


class Changes(SequenceOf):
    componentType = Change()


class DeleteOldRDN(Boolean):
    pass


class NewSuperior(LDAPDN):
    tagSet = LDAPDN.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))


class RequestName(LDAPOID):
    tagSet = LDAPOID.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))


class RequestValue(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))
    encoding = 'utf-8'


class ResponseName(LDAPOID):
    tagSet = LDAPOID.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 10))


class ResponseValue(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 11))
    encoding = 'utf-8'


class IntermediateResponseName(LDAPOID):
    tagSet = LDAPOID.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))


class IntermediateResponseValue(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))
    encoding = 'utf-8'


class BindRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 0))
    componentType = NamedTypes(NamedType('version', Version()), NamedType('name', LDAPDN()), NamedType('authentication', AuthenticationChoice()))


class BindResponse(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 1))
    componentType = NamedTypes(NamedType('resultCode', ResultCode()), NamedType('matchedDN', LDAPDN()), NamedType('diagnosticMessage', LDAPString()), OptionalNamedType('referral', Referral()), OptionalNamedType('serverSaslCreds', ServerSaslCreds()))


class UnbindRequest(Null):
    tagSet = Null.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatSimple, 2))


class SearchRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 3))
    componentType = NamedTypes(NamedType('baseObject', LDAPDN()), NamedType('scope', Scope()), NamedType('derefAliases', DerefAliases()), NamedType('sizeLimit', Integer0ToMax()), NamedType('timeLimit', Integer0ToMax()), NamedType('typesOnly', TypesOnly()), NamedType('filter', Filter()), NamedType('attributes', AttributeSelection()))


class SearchResultReference(SequenceOf):
    tagSet = SequenceOf.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 19))
    subtypeSpec = SequenceOf.subtypeSpec + size1ToMaxConstraint
    componentType = URI()


class SearchResultEntry(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 4))
    componentType = NamedTypes(NamedType('object', LDAPDN()), NamedType('attributes', PartialAttributeList()))


class SearchResultDone(LDAPResult):
    tagSet = LDAPResult.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 5))


class ModifyRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 6))
    componentType = NamedTypes(NamedType('object', LDAPDN()), NamedType('changes', Changes()))


class ModifyResponse(LDAPResult):
    tagSet = LDAPResult.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 7))


class AddRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 8))
    componentType = NamedTypes(NamedType('entry', LDAPDN()), NamedType('attributes', AttributeList()))


class AddResponse(LDAPResult):
    tagSet = LDAPResult.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 9))


class DelRequest(LDAPDN):
    tagSet = LDAPDN.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatSimple, 10))


class DelResponse(LDAPResult):
    tagSet = LDAPResult.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 11))


class ModifyDNRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 12))
    componentType = NamedTypes(NamedType('entry', LDAPDN()), NamedType('newrdn', RelativeLDAPDN()), NamedType('deleteoldrdn', DeleteOldRDN()), OptionalNamedType('newSuperior', NewSuperior()))


class ModifyDNResponse(LDAPResult):
    tagSet = LDAPResult.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 13))


class CompareRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 14))
    componentType = NamedTypes(NamedType('entry', LDAPDN()), NamedType('ava', AttributeValueAssertion()))


class CompareResponse(LDAPResult):
    tagSet = LDAPResult.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 15))


class AbandonRequest(MessageID):
    tagSet = MessageID.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatSimple, 16))


class ExtendedRequest(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 23))
    componentType = NamedTypes(NamedType('requestName', RequestName()), OptionalNamedType('requestValue', RequestValue()))


class ExtendedResponse(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 24))
    componentType = NamedTypes(NamedType('resultCode', ResultCode()), NamedType('matchedDN', LDAPDN()), NamedType('diagnosticMessage', LDAPString()), OptionalNamedType('referral', Referral()), OptionalNamedType('responseName', ResponseName()), OptionalNamedType('responseValue', ResponseValue()))


class IntermediateResponse(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 25))
    componentType = NamedTypes(OptionalNamedType('responseName', IntermediateResponseName()), OptionalNamedType('responseValue', IntermediateResponseValue()))


class ProtocolOp(Choice):
    componentType = NamedTypes(NamedType('bindRequest', BindRequest()), NamedType('bindResponse', BindResponse()), NamedType('unbindRequest', UnbindRequest()), NamedType('searchRequest', SearchRequest()), NamedType('searchResEntry', SearchResultEntry()), NamedType('searchResDone', SearchResultDone()), NamedType('searchResRef', SearchResultReference()), NamedType('modifyRequest', ModifyRequest()), NamedType('modifyResponse', ModifyResponse()), NamedType('addRequest', AddRequest()), NamedType('addResponse', AddResponse()), NamedType('delRequest', DelRequest()), NamedType('delResponse', DelResponse()), NamedType('modDNRequest', ModifyDNRequest()), NamedType('modDNResponse', ModifyDNResponse()), NamedType('compareRequest', CompareRequest()), NamedType('compareResponse', CompareResponse()), NamedType('abandonRequest', AbandonRequest()), NamedType('extendedReq', ExtendedRequest()), NamedType('extendedResp', ExtendedResponse()), NamedType('intermediateResponse', IntermediateResponse()))


class LDAPMessage(Sequence):
    componentType = NamedTypes(NamedType('messageID', MessageID()), NamedType('protocolOp', ProtocolOp()), OptionalNamedType('controls', Controls()))