# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc1422.py
# Compiled at: 2020-03-04 06:24:45
# Size of source mod 2**32: 7429 bytes
import arpa2.quickder as _api
from rfc3280 import Name

class AlgorithmIdentifier(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'algorithm':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'parameters':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class CertificateSerialNumber(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class CRLEntry(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'userCertificate':(
       '_TYPTR', ['CertificateSerialNumber'], 0), 
      'revocationDate':(
       '_TYPTR', ['_api.ASN1UTCTime'], 1)})
    _context = globals()
    _numcursori = 2


class Version(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
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


class Validity(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'notBefore':(
       '_TYPTR', ['_api.ASN1UTCTime'], 0), 
      'notAfter':(
       '_TYPTR', ['_api.ASN1UTCTime'], 1)})
    _context = globals()
    _numcursori = 2


class Certificate(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
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
       '_TYPTR', ['Name'], 7), 
      'subjectPublicKeyInfo':(
       '_TYPTR', ['SubjectPublicKeyInfo'], 8)})
    _context = globals()
    _numcursori = 11


class CertificateRevocationList(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'signature':(
       '_TYPTR', ['AlgorithmIdentifier'], 0), 
      'issuer':(
       '_TYPTR', ['Name'], 2), 
      'lastUpdate':(
       '_TYPTR', ['_api.ASN1UTCTime'], 3), 
      'nextUpdate':(
       '_TYPTR', ['_api.ASN1UTCTime'], 4), 
      'revokedCertificates':(
       '_SEQOF', 5,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_UTCTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_TYPTR', ['CRLEntry'], 0))})
    _context = globals()
    _numcursori = 6