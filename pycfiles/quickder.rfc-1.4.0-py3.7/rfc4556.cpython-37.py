# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc4556.py
# Compiled at: 2020-03-04 06:24:34
# Size of source mod 2**32: 18032 bytes
import arpa2.quickder as _api
from rfc3280 import SubjectPublicKeyInfo, AlgorithmIdentifier
from rfc4120 import KerberosTime, PrincipalName, Realm, EncryptionKey, Checksum

class ExternalPrincipalIdentifier(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'subjectName':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'issuerAndSerialNumber':(
       '_TYPTR', ['_api.ASN1OctetString'], 1), 
      'subjectKeyIdentifier':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class AD_INITIAL_VERIFIED_CAS(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['ExternalPrincipalIdentifier'], 0))
    _context = globals()
    _numcursori = 1


class PKAuthenticator(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'cusec':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'ctime':(
       '_TYPTR', ['KerberosTime'], 1), 
      'nonce':(
       '_TYPTR', ['_api.ASN1Integer'], 2), 
      'paChecksum':(
       '_TYPTR', ['_api.ASN1OctetString'], 3)})
    _context = globals()
    _numcursori = 4


class DHNonce(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class AuthPack(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pkAuthenticator':(
       '_TYPTR', ['PKAuthenticator'], 0), 
      'clientPublicValue':(
       '_TYPTR', ['SubjectPublicKeyInfo'], 4), 
      'supportedCMSTypes':(
       '_SEQOF', 7,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_TYPTR', ['AlgorithmIdentifier'], 0)), 
      'clientDHNonce':(
       '_TYPTR', ['DHNonce'], 8)})
    _context = globals()
    _numcursori = 9


class DHRepInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'dhSignedData':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'serverDHNonce':(
       '_TYPTR', ['DHNonce'], 1)})
    _context = globals()
    _numcursori = 2


class KDCDHKeyInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'subjectPublicKey':(
       '_TYPTR', ['_api.ASN1BitString'], 0), 
      'nonce':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'dhKeyExpiration':(
       '_TYPTR', ['KerberosTime'], 2)})
    _context = globals()
    _numcursori = 3


class KRB5PrincipalName(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'realm':(
       '_TYPTR', ['Realm'], 0), 
      'principalName':(
       '_TYPTR', ['PrincipalName'], 1)})
    _context = globals()
    _numcursori = 3


class PA_PK_AS_REP(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'dhInfo':(
       '_TYPTR', ['DHRepInfo'], 0), 
      'encKeyPack':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class PA_PK_AS_REQ(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'signedAuthPack':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'trustedCertifiers':(
       '_SEQOF', 1,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
       (
        '_TYPTR', ['ExternalPrincipalIdentifier'], 0)), 
      'kdcPkId':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class ReplyKeyPack(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'replyKey':(
       '_TYPTR', ['EncryptionKey'], 0), 
      'asChecksum':(
       '_TYPTR', ['Checksum'], 2)})
    _context = globals()
    _numcursori = 4


class TD_DH_PARAMETERS(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['AlgorithmIdentifier'], 0))
    _context = globals()
    _numcursori = 1


class TD_INVALID_CERTIFICATES(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['ExternalPrincipalIdentifier'], 0))
    _context = globals()
    _numcursori = 1


class TD_TRUSTED_CERTIFIERS(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['ExternalPrincipalIdentifier'], 0))
    _context = globals()
    _numcursori = 1


ad_initial_verified_cas = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(9)], context={})
id_pkinit = _api.ASN1OID(bindata=[_api.der_format_OID('1.3.6.1.5.2.3')], context={})
id_pkinit_DHKeyData = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkinit.get()) + '.2')], context={})
id_pkinit_KPClientAuth = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkinit.get()) + '.4')], context={})
id_pkinit_KPKdc = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkinit.get()) + '.5')], context={})
id_pkinit_authData = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkinit.get()) + '.1')], context={})
id_pkinit_rkeyData = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(id_pkinit.get()) + '.3')], context={})
id_pkinit_san = _api.ASN1OID(bindata=[_api.der_format_OID('1.3.6.1.5.2.2')], context={})
pa_pk_as_rep = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(17)], context={})
pa_pk_as_req = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(16)], context={})
td_dh_parameters = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(109)], context={})
td_invalid_certificates = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(105)], context={})
td_trusted_certifiers = _api.ASN1Integer(bindata=[_api.der_format_INTEGER(104)], context={})