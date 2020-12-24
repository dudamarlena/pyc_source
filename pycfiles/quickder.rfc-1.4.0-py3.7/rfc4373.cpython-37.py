# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc4373.py
# Compiled at: 2020-03-04 06:24:43
# Size of source mod 2**32: 9584 bytes
import arpa2.quickder as _api
from rfc4511 import LDAPOID, LDAPResult, LDAPDN, LDAPString, Referral, Controls, AddRequest, ModifyRequest, DelRequest, ModifyDNRequest

class EndLBURPRequestValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'sequenceNumber': ('_TYPTR', ['_api.ASN1Integer'], 0)})
    _context = globals()
    _numcursori = 1


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
      'response':(
       '_TYPTR', ['_api.ASN1OctetString'], 5)})
    _context = globals()
    _numcursori = 6


class UpdateOperationList(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(12)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 10,
     (
      '_NAMED',
      {'updateOperation':(
        '_NAMED',
        {'addRequest':(
          '_TYPTR', ['AddRequest'], 0), 
         'modifyRequest':(
          '_TYPTR', ['ModifyRequest'], 2), 
         'delRequest':(
          '_TYPTR', ['DelRequest'], 4), 
         'modDNRequest':(
          '_TYPTR', ['ModifyDNRequest'], 5)}), 
       'controls':(
        '_TYPTR', ['Controls'], 9)}))
    _context = globals()
    _numcursori = 1


class LBURPUpdateRequestValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'sequenceNumber':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'updateOperationList':(
       '_TYPTR', ['UpdateOperationList'], 1)})
    _context = globals()
    _numcursori = 2


class MaxOperations(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class OperationResult(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'operationNumber':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'ldapResult':(
       '_TYPTR', ['LDAPResult'], 1)})
    _context = globals()
    _numcursori = 5


class OperationResults(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_ENUMERATED) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 5,
     (
      '_TYPTR', ['OperationResult'], 0))
    _context = globals()
    _numcursori = 1


class StartLBURPRequestValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'updateStyleOID': ('_TYPTR', ['LDAPOID'], 0)})
    _context = globals()
    _numcursori = 1


class StartLBURPResponseValue(MaxOperations):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['MaxOperations'], 0)
    _context = globals()
    _numcursori = 1


maxInt = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(2147483647)], context={})