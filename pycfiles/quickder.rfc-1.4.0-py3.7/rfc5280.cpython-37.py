# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc5280.py
# Compiled at: 2020-03-04 06:24:39
# Size of source mod 2**32: 80243 bytes
import arpa2.quickder as _api

class OtherName(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type_id':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'value':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class DirectoryString(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'teletexString':(
       '_TYPTR', ['_api.ASN1TeletexString'], 0), 
      'printableString':(
       '_TYPTR', ['_api.ASN1PrintableString'], 1), 
      'universalString':(
       '_TYPTR', ['_api.ASN1UniversalString'], 2), 
      'utf8String':(
       '_TYPTR', ['_api.ASN1UTF8String'], 3), 
      'bmpString':4})
    _context = globals()
    _numcursori = 5


class EDIPartyName(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'nameAssigner':(
       '_TYPTR', ['DirectoryString'], 0), 
      'partyName':(
       '_TYPTR', ['DirectoryString'], 5)})
    _context = globals()
    _numcursori = 10


class AttributeValue(_api.ASN1Any):
    _der_packer = chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Any'], 0)
    _context = globals()
    _numcursori = 1


class AttributeType(_api.ASN1OID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OID'], 0)
    _context = globals()
    _numcursori = 1


class AttributeTypeAndValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type':(
       '_TYPTR', ['AttributeType'], 0), 
      'value':(
       '_TYPTR', ['AttributeValue'], 1)})
    _context = globals()
    _numcursori = 2


class RelativeDistinguishedName(_api.ASN1SetOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_END)
    _recipe = ('_SETOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['AttributeTypeAndValue'], 0))
    _context = globals()
    _numcursori = 1


class RDNSequence(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_END), 1,
     (
      '_TYPTR', ['RelativeDistinguishedName'], 0))
    _context = globals()
    _numcursori = 1


class Name(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'rdnSequence': ('_TYPTR', ['RDNSequence'], 0)})
    _context = globals()
    _numcursori = 1


class GeneralName(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'otherName':(
       '_TYPTR', ['OtherName'], 0), 
      'rfc822Name':(
       '_TYPTR', ['_api.ASN1IA5String'], 2), 
      'dNSName':(
       '_TYPTR', ['_api.ASN1IA5String'], 3), 
      'directoryName':(
       '_TYPTR', ['Name'], 4), 
      'ediPartyName':(
       '_TYPTR', ['EDIPartyName'], 5), 
      'uniformResourceIdentifier':(
       '_TYPTR', ['_api.ASN1IA5String'], 15), 
      'iPAddress':(
       '_TYPTR', ['_api.ASN1OctetString'], 16), 
      'registeredID':(
       '_TYPTR', ['_api.ASN1OID'], 17)})
    _context = globals()
    _numcursori = 18


class AccessDescription(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'accessMethod':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'accessLocation':(
       '_TYPTR', ['GeneralName'], 1)})
    _context = globals()
    _numcursori = 19


class AlgorithmIdentifier(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'algorithm':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'parameters':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class Attribute(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type':(
       '_TYPTR', ['AttributeType'], 0), 
      'values':(
       '_SETOF', 1,
       chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['AttributeValue'], 0))})
    _context = globals()
    _numcursori = 2


class AuthorityInfoAccessSyntax(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 19,
     (
      '_TYPTR', ['AccessDescription'], 0))
    _context = globals()
    _numcursori = 1


class KeyIdentifier(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class CertificateSerialNumber(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class GeneralNames(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END), 18,
     (
      '_TYPTR', ['GeneralName'], 0))
    _context = globals()
    _numcursori = 1


class AuthorityKeyIdentifier(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'keyIdentifier':(
       '_TYPTR', ['KeyIdentifier'], 0), 
      'authorityCertIssuer':(
       '_TYPTR', ['GeneralNames'], 1), 
      'authorityCertSerialNumber':(
       '_TYPTR', ['CertificateSerialNumber'], 2)})
    _context = globals()
    _numcursori = 3


class CRLNumber(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class BaseCRLNumber(CRLNumber):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['CRLNumber'], 0)
    _context = globals()
    _numcursori = 1


class BaseDistance(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class BasicConstraints(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'cA':(
       '_TYPTR', ['_api.ASN1Boolean'], 0), 
      'pathLenConstraint':(
       '_TYPTR', ['_api.ASN1Integer'], 1)})
    _context = globals()
    _numcursori = 2


class CPSuri(_api.ASN1IA5String):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1IA5String'], 0)
    _context = globals()
    _numcursori = 1


class DistributionPointName(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'fullName':(
       '_TYPTR', ['GeneralNames'], 0), 
      'nameRelativeToCRLIssuer':(
       '_TYPTR', ['RelativeDistinguishedName'], 1)})
    _context = globals()
    _numcursori = 2


class ReasonFlags(_api.ASN1BitString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1BitString'], 0)
    _context = globals()
    _numcursori = 1


class DistributionPoint(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'distributionPoint':(
       '_TYPTR', ['DistributionPointName'], 0), 
      'reasons':(
       '_TYPTR', ['ReasonFlags'], 2), 
      'cRLIssuer':(
       '_TYPTR', ['GeneralNames'], 3)})
    _context = globals()
    _numcursori = 4


class CRLDistributionPoints(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 4,
     (
      '_TYPTR', ['DistributionPoint'], 0))
    _context = globals()
    _numcursori = 1


class CRLReason(_api.ASN1Enumerated):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Enumerated'], 0)
    _context = globals()
    _numcursori = 1


class CertPolicyId(_api.ASN1OID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OID'], 0)
    _context = globals()
    _numcursori = 1


class Extension(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'extnID':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'critical':(
       '_TYPTR', ['_api.ASN1Boolean'], 1), 
      'extnValue':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class Extensions(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['Extension'], 0))
    _context = globals()
    _numcursori = 1


class Version(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class UniqueIdentifier(_api.ASN1BitString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1BitString'], 0)
    _context = globals()
    _numcursori = 1


class SubjectPublicKeyInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'algorithm':(
       '_TYPTR', ['AlgorithmIdentifier'], 0), 
      'subjectPublicKey':(
       '_TYPTR', ['_api.ASN1BitString'], 2)})
    _context = globals()
    _numcursori = 3


class Time(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'utcTime':(
       '_TYPTR', ['_api.ASN1UTCTime'], 0), 
      'generalTime':(
       '_TYPTR', ['_api.ASN1GeneralizedTime'], 1)})
    _context = globals()
    _numcursori = 2


class Validity(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'notBefore':(
       '_TYPTR', ['Time'], 0), 
      'notAfter':(
       '_TYPTR', ['Time'], 2)})
    _context = globals()
    _numcursori = 4


class TBSCertificate(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'version':(
       '_TYPTR', ['Version'], 0), 
      'serialNumber':(
       '_TYPTR', ['CertificateSerialNumber'], 1), 
      'signature':(
       '_TYPTR', ['AlgorithmIdentifier'], 2), 
      'issuer':(
       '_TYPTR', ['Name'], 4), 
      'validity':(
       '_TYPTR', ['Validity'], 5), 
      'subject':(
       '_TYPTR', ['Name'], 9), 
      'subjectPublicKeyInfo':(
       '_TYPTR', ['SubjectPublicKeyInfo'], 10), 
      'issuerUniqueID':(
       '_TYPTR', ['UniqueIdentifier'], 13), 
      'subjectUniqueID':(
       '_TYPTR', ['UniqueIdentifier'], 14), 
      'extensions':(
       '_TYPTR', ['Extensions'], 15)})
    _context = globals()
    _numcursori = 16


class Certificate(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'tbsCertificate':(
       '_TYPTR', ['TBSCertificate'], 0), 
      'signatureAlgorithm':(
       '_TYPTR', ['AlgorithmIdentifier'], 16), 
      'signatureValue':(
       '_TYPTR', ['_api.ASN1BitString'], 18)})
    _context = globals()
    _numcursori = 19


class CertificateIssuer(GeneralNames):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['GeneralNames'], 0)
    _context = globals()
    _numcursori = 1


class TBSCertList(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'version':(
       '_TYPTR', ['Version'], 0), 
      'signature':(
       '_TYPTR', ['AlgorithmIdentifier'], 1), 
      'issuer':(
       '_TYPTR', ['Name'], 3), 
      'thisUpdate':(
       '_TYPTR', ['Time'], 4), 
      'nextUpdate':(
       '_TYPTR', ['Time'], 6), 
      'revokedCertificates':(
       '_SEQOF', 8,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 4,
       (
        '_NAMED',
        {'userCertificate':(
          '_TYPTR', ['CertificateSerialNumber'], 0), 
         'revocationDate':(
          '_TYPTR', ['Time'], 1), 
         'crlEntryExtensions':(
          '_TYPTR', ['Extensions'], 3)})), 
      'crlExtensions':(
       '_TYPTR', ['Extensions'], 9)})
    _context = globals()
    _numcursori = 10


class CertificateList(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'tbsCertList':(
       '_TYPTR', ['TBSCertList'], 0), 
      'signatureAlgorithm':(
       '_TYPTR', ['AlgorithmIdentifier'], 10), 
      'signatureValue':(
       '_TYPTR', ['_api.ASN1BitString'], 12)})
    _context = globals()
    _numcursori = 13


class PolicyQualifierId(_api.ASN1OID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OID'], 0)
    _context = globals()
    _numcursori = 1


class PolicyQualifierInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'policyQualifierId':(
       '_TYPTR', ['PolicyQualifierId'], 0), 
      'qualifier':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class PolicyInformation(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'policyIdentifier':(
       '_TYPTR', ['CertPolicyId'], 0), 
      'policyQualifiers':(
       '_SEQOF', 1,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_TYPTR', ['PolicyQualifierInfo'], 0))})
    _context = globals()
    _numcursori = 2


class CertificatePolicies(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['PolicyInformation'], 0))
    _context = globals()
    _numcursori = 1


class DisplayText(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_VISIBLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'ia5String':(
       '_TYPTR', ['_api.ASN1IA5String'], 0), 
      'visibleString':(
       '_TYPTR', ['_api.ASN1VisibleString'], 1), 
      'bmpString':2, 
      'utf8String':(
       '_TYPTR', ['_api.ASN1UTF8String'], 3)})
    _context = globals()
    _numcursori = 4


class KeyPurposeId(_api.ASN1OID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OID'], 0)
    _context = globals()
    _numcursori = 1


class ExtKeyUsageSyntax(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END), 1,
     (
      '_TYPTR', ['KeyPurposeId'], 0))
    _context = globals()
    _numcursori = 1


class FreshestCRL(CRLDistributionPoints):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['CRLDistributionPoints'], 0)
    _context = globals()
    _numcursori = 1


class FreshestCRL(CRLDistributionPoints):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['CRLDistributionPoints'], 0)
    _context = globals()
    _numcursori = 1


class GeneralSubtree(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'base':(
       '_TYPTR', ['GeneralName'], 0), 
      'minimum':(
       '_TYPTR', ['BaseDistance'], 18), 
      'maximum':(
       '_TYPTR', ['BaseDistance'], 19)})
    _context = globals()
    _numcursori = 20


class GeneralSubtrees(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 20,
     (
      '_TYPTR', ['GeneralSubtree'], 0))
    _context = globals()
    _numcursori = 1


class SkipCerts(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class InhibitAnyPolicy(SkipCerts):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['SkipCerts'], 0)
    _context = globals()
    _numcursori = 1


class InvalidityDate(_api.ASN1GeneralizedTime):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1GeneralizedTime'], 0)
    _context = globals()
    _numcursori = 1


class IssuerAltName(GeneralNames):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['GeneralNames'], 0)
    _context = globals()
    _numcursori = 1


class IssuingDistributionPoint(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'distributionPoint':(
       '_TYPTR', ['DistributionPointName'], 0), 
      'onlyContainsUserCerts':(
       '_TYPTR', ['_api.ASN1Boolean'], 2), 
      'onlyContainsCACerts':(
       '_TYPTR', ['_api.ASN1Boolean'], 3), 
      'onlySomeReasons':(
       '_TYPTR', ['ReasonFlags'], 4), 
      'indirectCRL':(
       '_TYPTR', ['_api.ASN1Boolean'], 5), 
      'onlyContainsAttributeCerts':(
       '_TYPTR', ['_api.ASN1Boolean'], 6)})
    _context = globals()
    _numcursori = 7


class KeyUsage(_api.ASN1BitString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1BitString'], 0)
    _context = globals()
    _numcursori = 1


class NameConstraints(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'permittedSubtrees':(
       '_TYPTR', ['GeneralSubtrees'], 0), 
      'excludedSubtrees':(
       '_TYPTR', ['GeneralSubtrees'], 1)})
    _context = globals()
    _numcursori = 2


class NoticeReference(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_VISIBLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'organization':(
       '_TYPTR', ['DisplayText'], 0), 
      'noticeNumbers':(
       '_SEQOF', 4,
       chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['_api.ASN1Integer'], 0))})
    _context = globals()
    _numcursori = 5


class PolicyConstraints(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'requireExplicitPolicy':(
       '_TYPTR', ['SkipCerts'], 0), 
      'inhibitPolicyMapping':(
       '_TYPTR', ['SkipCerts'], 1)})
    _context = globals()
    _numcursori = 2


class PolicyMappings(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_NAMED',
      {'issuerDomainPolicy':(
        '_TYPTR', ['CertPolicyId'], 0), 
       'subjectDomainPolicy':(
        '_TYPTR', ['CertPolicyId'], 1)}))
    _context = globals()
    _numcursori = 1


class UserNotice(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_VISIBLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_VISIBLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'noticeRef':(
       '_TYPTR', ['NoticeReference'], 0), 
      'explicitText':(
       '_TYPTR', ['DisplayText'], 5)})
    _context = globals()
    _numcursori = 9


class Qualifier(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_VISIBLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_VISIBLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'cPSuri':(
       '_TYPTR', ['CPSuri'], 0), 
      'userNotice':(
       '_TYPTR', ['UserNotice'], 1)})
    _context = globals()
    _numcursori = 10


class SkipCerts(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class SubjectAltName(GeneralNames):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['GeneralNames'], 0)
    _context = globals()
    _numcursori = 1


class SubjectDirectoryAttributes(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['Attribute'], 0))
    _context = globals()
    _numcursori = 1


class SubjectInfoAccessSyntax(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_TELETEXSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_PRINTABLESTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UNIVERSALSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTF8STRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BMPSTRING) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_IA5STRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 19,
     (
      '_TYPTR', ['AccessDescription'], 0))
    _context = globals()
    _numcursori = 1


class SubjectKeyIdentifier(KeyIdentifier):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KeyIdentifier'], 0)
    _context = globals()
    _numcursori = 1


id_ce = _api.ASN1OID(bindata=[_api.der_format_OID('2.5.29')], context={})
id_ce_extKeyUsage = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.37')], context={})
anyExtendedKeyUsage = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce_extKeyUsage.get()) + '.0')], context={})
id_ce_certificatePolicies = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.32')], context={})
anyPolicy = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce_certificatePolicies.get()) + '.0')], context={})
id_pkix = _api.ASN1OID(bindata=[_api.der_format_OID('1.3.6.1.5.5.7')], context={})
id_ad = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkix.get()) + '.48')], context={})
id_ad_caIssuers = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ad.get()) + '.2')], context={})
id_ad_caRepository = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ad.get()) + '.5')], context={})
id_ad_ocsp = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ad.get()) + '.1')], context={})
id_ad_timeStamping = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ad.get()) + '.3')], context={})
id_ce_authorityKeyIdentifier = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.35')], context={})
id_ce_basicConstraints = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.19')], context={})
id_ce_cRLDistributionPoints = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.31')], context={})
id_ce_cRLNumber = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.20')], context={})
id_ce_cRLReasons = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.21')], context={})
id_ce_certificateIssuer = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.29')], context={})
id_ce_deltaCRLIndicator = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.27')], context={})
id_ce_freshestCRL = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.46')], context={})
id_ce_freshestCRL = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.46')], context={})
id_ce_inhibitAnyPolicy = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.54')], context={})
id_ce_invalidityDate = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.24')], context={})
id_ce_issuerAltName = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.18')], context={})
id_ce_issuingDistributionPoint = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.28')], context={})
id_ce_keyUsage = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.15')], context={})
id_ce_nameConstraints = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.30')], context={})
id_ce_policyConstraints = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.36')], context={})
id_ce_policyMappings = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.33')], context={})
id_ce_subjectAltName = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.17')], context={})
id_ce_subjectDirectoryAttributes = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.9')], context={})
id_ce_subjectKeyIdentifier = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_ce.get()) + '.14')], context={})
id_kp = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkix.get()) + '.3')], context={})
id_kp_OCSPSigning = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_kp.get()) + '.9')], context={})
id_kp_clientAuth = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_kp.get()) + '.2')], context={})
id_kp_codeSigning = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_kp.get()) + '.3')], context={})
id_kp_emailProtection = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_kp.get()) + '.4')], context={})
id_kp_serverAuth = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_kp.get()) + '.1')], context={})
id_kp_timeStamping = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_kp.get()) + '.8')], context={})
id_pe = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkix.get()) + '.1')], context={})
id_pe_authorityInfoAccess = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pe.get()) + '.1')], context={})
id_pe_subjectInfoAccess = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pe.get()) + '.11')], context={})
id_qt = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkix.get()) + '.2')], context={})
id_qt_cps = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_qt.get()) + '.1')], context={})
id_qt_unotice = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_qt.get()) + '.2')], context={})