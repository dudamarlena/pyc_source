# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc4511.py
# Compiled at: 2020-03-04 06:24:36
# Size of source mod 2**32: 45131 bytes
import arpa2.quickder as _api

class MessageID(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class AbandonRequest(MessageID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(16)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['MessageID'], 0)
    _context = globals()
    _numcursori = 1


class LDAPString(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class AttributeDescription(LDAPString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPString'], 0)
    _context = globals()
    _numcursori = 1


class AttributeValue(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class Attribute(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type':(
       '_TYPTR', ['AttributeDescription'], 0), 
      'vals':(
       '_SETOF', 1,
       chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['AttributeValue'], 0))})
    _context = globals()
    _numcursori = 2


class AttributeList(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['Attribute'], 0))
    _context = globals()
    _numcursori = 1


class LDAPDN(LDAPString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPString'], 0)
    _context = globals()
    _numcursori = 1


class AddRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'entry':(
       '_TYPTR', ['LDAPDN'], 0), 
      'attributes':(
       '_TYPTR', ['AttributeList'], 1)})
    _context = globals()
    _numcursori = 2


class URI(LDAPString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPString'], 0)
    _context = globals()
    _numcursori = 1


class Referral(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END), 1,
     (
      '_TYPTR', ['URI'], 0))
    _context = globals()
    _numcursori = 1


class LDAPResult(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'resultCode':(
       '_TYPTR', ['_api.ASN1Enumerated'], 0), 
      'matchedDN':(
       '_TYPTR', ['LDAPDN'], 1), 
      'diagnosticMessage':(
       '_TYPTR', ['LDAPString'], 2), 
      'referral':(
       '_TYPTR', ['Referral'], 3)})
    _context = globals()
    _numcursori = 4


class AddResponse(LDAPResult):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPResult'], 0)
    _context = globals()
    _numcursori = 4


class AssertionValue(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class AttributeSelection(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END), 1,
     (
      '_TYPTR', ['LDAPString'], 0))
    _context = globals()
    _numcursori = 1


class AttributeValueAssertion(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'attributeDesc':(
       '_TYPTR', ['AttributeDescription'], 0), 
      'assertionValue':(
       '_TYPTR', ['AssertionValue'], 1)})
    _context = globals()
    _numcursori = 2


class SaslCredentials(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'mechanism':(
       '_TYPTR', ['LDAPString'], 0), 
      'credentials':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class AuthenticationChoice(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'simple':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'sasl':(
       '_TYPTR', ['SaslCredentials'], 1)})
    _context = globals()
    _numcursori = 3


class BindRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'version':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'name':(
       '_TYPTR', ['LDAPDN'], 1), 
      'authentication':(
       '_TYPTR', ['AuthenticationChoice'], 2)})
    _context = globals()
    _numcursori = 5


class BindResponse(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'resultCode':(
       '_TYPTR', ['_api.ASN1Enumerated'], 0), 
      'matchedDN':(
       '_TYPTR', ['LDAPDN'], 1), 
      'diagnosticMessage':(
       '_TYPTR', ['LDAPString'], 2), 
      'referral':(
       '_TYPTR', ['Referral'], 3), 
      'serverSaslCreds':(
       '_TYPTR', ['_api.ASN1OctetString'], 4)})
    _context = globals()
    _numcursori = 5


class CompareRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(14)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'entry':(
       '_TYPTR', ['LDAPDN'], 0), 
      'ava':(
       '_TYPTR', ['AttributeValueAssertion'], 1)})
    _context = globals()
    _numcursori = 3


class CompareResponse(LDAPResult):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(15)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPResult'], 0)
    _context = globals()
    _numcursori = 4


class LDAPOID(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class Control(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'controlType':(
       '_TYPTR', ['LDAPOID'], 0), 
      'criticality':(
       '_TYPTR', ['_api.ASN1Boolean'], 1), 
      'controlValue':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class Controls(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['Control'], 0))
    _context = globals()
    _numcursori = 1


class DelRequest(LDAPDN):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(10)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPDN'], 0)
    _context = globals()
    _numcursori = 1


class DelResponse(LDAPResult):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPResult'], 0)
    _context = globals()
    _numcursori = 4


class ExtendedRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(23)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'requestName':(
       '_TYPTR', ['LDAPOID'], 0), 
      'requestValue':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class ExtendedResponse(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(24)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'resultCode':(
       '_TYPTR', ['_api.ASN1Enumerated'], 0), 
      'matchedDN':(
       '_TYPTR', ['LDAPDN'], 1), 
      'diagnosticMessage':(
       '_TYPTR', ['LDAPString'], 2), 
      'referral':(
       '_TYPTR', ['Referral'], 3), 
      'responseName':(
       '_TYPTR', ['LDAPOID'], 4), 
      'responseValue':(
       '_TYPTR', ['_api.ASN1OctetString'], 5)})
    _context = globals()
    _numcursori = 6


class Filter(_api.ASN1Any):
    _der_packer = chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Any'], 0)
    _context = globals()
    _numcursori = 1


class SubstringFilter(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type':(
       '_TYPTR', ['AttributeDescription'], 0), 
      'substrings':(
       '_SEQOF', 1,
       chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END), 3,
       (
        '_NAMED',
        {'initial':(
          '_TYPTR', ['AssertionValue'], 0), 
         'any':(
          '_TYPTR', ['AssertionValue'], 1), 
         'final':(
          '_TYPTR', ['AssertionValue'], 2)}))})
    _context = globals()
    _numcursori = 2


class MatchingRuleId(LDAPString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPString'], 0)
    _context = globals()
    _numcursori = 1


class MatchingRuleAssertion(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'matchingRule':(
       '_TYPTR', ['MatchingRuleId'], 0), 
      'type':(
       '_TYPTR', ['AttributeDescription'], 1), 
      'matchValue':(
       '_TYPTR', ['AssertionValue'], 2), 
      'dnAttributes':(
       '_TYPTR', ['_api.ASN1Boolean'], 3)})
    _context = globals()
    _numcursori = 4


class FilterOperation(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'andFilter':(
       '_SETOF', 0,
       chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['Filter'], 0)), 
      'orFilter':(
       '_SETOF', 1,
       chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['Filter'], 0)), 
      'notFilter':(
       '_TYPTR', ['Filter'], 2), 
      'equalityMatch':(
       '_TYPTR', ['AttributeValueAssertion'], 3), 
      'substrings':(
       '_TYPTR', ['SubstringFilter'], 5), 
      'greaterOrEqual':(
       '_TYPTR', ['AttributeValueAssertion'], 7), 
      'lessOrEqual':(
       '_TYPTR', ['AttributeValueAssertion'], 9), 
      'present':(
       '_TYPTR', ['AttributeDescription'], 11), 
      'approxMatch':(
       '_TYPTR', ['AttributeValueAssertion'], 12), 
      'extensibleMatch':(
       '_TYPTR', ['MatchingRuleAssertion'], 14)})
    _context = globals()
    _numcursori = 18


class IntermediateResponse(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(25)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'responseName':(
       '_TYPTR', ['LDAPOID'], 0), 
      'responseValue':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class SearchResultDone(LDAPResult):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPResult'], 0)
    _context = globals()
    _numcursori = 4


class UnbindRequest(_api.ASN1Null):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Null'], 0)
    _context = globals()
    _numcursori = 1


class PartialAttribute(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type':(
       '_TYPTR', ['AttributeDescription'], 0), 
      'vals':(
       '_SETOF', 1,
       chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['AttributeValue'], 0))})
    _context = globals()
    _numcursori = 2


class PartialAttributeList(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['PartialAttribute'], 0))
    _context = globals()
    _numcursori = 1


class SearchResultEntry(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'objectName':(
       '_TYPTR', ['LDAPDN'], 0), 
      'attributes':(
       '_TYPTR', ['PartialAttributeList'], 1)})
    _context = globals()
    _numcursori = 2


class ModifyDNResponse(LDAPResult):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(13)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPResult'], 0)
    _context = globals()
    _numcursori = 4


class ModifyRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'object':(
       '_TYPTR', ['LDAPDN'], 0), 
      'changes':(
       '_SEQOF', 1,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
       (
        '_NAMED',
        {'operation':(
          '_TYPTR', ['_api.ASN1Enumerated'], 0), 
         'modification':(
          '_TYPTR', ['PartialAttribute'], 1)}))})
    _context = globals()
    _numcursori = 2


class RelativeLDAPDN(LDAPString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPString'], 0)
    _context = globals()
    _numcursori = 1


class ModifyDNRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(12)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'entry':(
       '_TYPTR', ['LDAPDN'], 0), 
      'newrdn':(
       '_TYPTR', ['RelativeLDAPDN'], 1), 
      'deleteoldrdn':(
       '_TYPTR', ['_api.ASN1Boolean'], 2), 
      'newSuperior':(
       '_TYPTR', ['LDAPDN'], 3)})
    _context = globals()
    _numcursori = 4


class SearchResultReference(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(19)) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END), 1,
     (
      '_TYPTR', ['URI'], 0))
    _context = globals()
    _numcursori = 1


class ModifyResponse(LDAPResult):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['LDAPResult'], 0)
    _context = globals()
    _numcursori = 4


class SearchRequest(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'baseObject':(
       '_TYPTR', ['LDAPDN'], 0), 
      'scope':(
       '_TYPTR', ['_api.ASN1Enumerated'], 1), 
      'derefAliases':(
       '_TYPTR', ['_api.ASN1Enumerated'], 2), 
      'sizeLimit':(
       '_TYPTR', ['_api.ASN1Integer'], 3), 
      'timeLimit':(
       '_TYPTR', ['_api.ASN1Integer'], 4), 
      'typesOnly':(
       '_TYPTR', ['_api.ASN1Boolean'], 5), 
      'filter':(
       '_TYPTR', ['_api.ASN1Any'], 6), 
      'attributes':(
       '_TYPTR', ['AttributeSelection'], 7)})
    _context = globals()
    _numcursori = 8


class LDAPMessage(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(19)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(12)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(13)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(14)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(15)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(16)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(23)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(24)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(25)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'messageID':(
       '_TYPTR', ['MessageID'], 0), 
      'protocolOp':(
       '_NAMED',
       {'bindRequest':(
         '_TYPTR', ['BindRequest'], 1), 
        'bindResponse':(
         '_TYPTR', ['BindResponse'], 6), 
        'unbindRequest':(
         '_TYPTR', ['UnbindRequest'], 11), 
        'searchRequest':(
         '_TYPTR', ['SearchRequest'], 12), 
        'searchResEntry':(
         '_TYPTR', ['SearchResultEntry'], 20), 
        'searchResDone':(
         '_TYPTR', ['SearchResultDone'], 22), 
        'searchResRef':(
         '_TYPTR', ['SearchResultReference'], 26), 
        'modifyRequest':(
         '_TYPTR', ['ModifyRequest'], 27), 
        'modifyResponse':(
         '_TYPTR', ['ModifyResponse'], 29), 
        'addRequest':(
         '_TYPTR', ['AddRequest'], 33), 
        'addResponse':(
         '_TYPTR', ['AddResponse'], 35), 
        'delRequest':(
         '_TYPTR', ['DelRequest'], 39), 
        'delResponse':(
         '_TYPTR', ['DelResponse'], 40), 
        'modDNRequest':(
         '_TYPTR', ['ModifyDNRequest'], 44), 
        'modDNResponse':(
         '_TYPTR', ['ModifyDNResponse'], 48), 
        'compareRequest':(
         '_TYPTR', ['CompareRequest'], 52), 
        'compareResponse':(
         '_TYPTR', ['CompareResponse'], 55), 
        'abandonRequest':(
         '_TYPTR', ['AbandonRequest'], 59), 
        'extendedReq':(
         '_TYPTR', ['ExtendedRequest'], 60), 
        'extendedResp':(
         '_TYPTR', ['ExtendedResponse'], 62), 
        'intermediateResponse':(
         '_TYPTR', ['IntermediateResponse'], 68)}), 
      'controls':(
       '_TYPTR', ['Controls'], 70)})
    _context = globals()
    _numcursori = 71


maxInt = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(2147483647)], context={})