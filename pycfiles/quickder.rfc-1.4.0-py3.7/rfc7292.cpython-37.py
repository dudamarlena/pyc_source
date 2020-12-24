# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc7292.py
# Compiled at: 2020-03-04 06:24:41
# Size of source mod 2**32: 11765 bytes
import arpa2.quickder as _api
from rfc2315 import ContentInfo, DigestInfo
from rfc5208 import PrivateKeyInfo, EncryptedPrivateKeyInfo

class AuthenticatedSafe(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['ContentInfo'], 0))
    _context = globals()
    _numcursori = 1


class CRLBag(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'crlId':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'crltValue':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class CertBag(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'certId':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'certValue':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class KeyBag(PrivateKeyInfo):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['PrivateKeyInfo'], 0)
    _context = globals()
    _numcursori = 5


class MacData(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'mac':(
       '_TYPTR', ['DigestInfo'], 0), 
      'macSalt':(
       '_TYPTR', ['_api.ASN1OctetString'], 3), 
      'iterations':(
       '_TYPTR', ['_api.ASN1Integer'], 4)})
    _context = globals()
    _numcursori = 5


class PFX(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'version':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'authSafe':(
       '_TYPTR', ['ContentInfo'], 1), 
      'macData':(
       '_TYPTR', ['MacData'], 3)})
    _context = globals()
    _numcursori = 8


class PKCS12Attribute(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'attrId':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'attrValues':(
       '_SETOF', 1,
       chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['_api.ASN1Any'], 0))})
    _context = globals()
    _numcursori = 2


class PKCS8ShroudedKeyBag(EncryptedPrivateKeyInfo):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['EncryptedPrivateKeyInfo'], 0)
    _context = globals()
    _numcursori = 3


class SafeBag(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'bagId':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'bagValue':(
       '_TYPTR', ['_api.ASN1Any'], 1), 
      'bagAttributes':(
       '_SETOF', 2,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_TYPTR', ['PKCS12Attribute'], 0))})
    _context = globals()
    _numcursori = 3


class SafeContents(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['SafeBag'], 0))
    _context = globals()
    _numcursori = 1


class SecretBag(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'secretTypeId':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'secretValue':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


rsadsi = _api.ASN1OID(bindata=[_api.der_format_OID('1.2.840.113549')], context={})
pkcs = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(rsadsi.get()) + '.1')], context={})
pkcs_12 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs.get()) + '.12')], context={})
bagtypes = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12.get()) + '.10.1')], context={})
pkcs_12PbeIds = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12.get()) + '.1')], context={})
pbeWithSHAAnd128BitRC2_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12PbeIds.get()) + '.5')], context={})
pbeWithSHAAnd128BitRC4 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12PbeIds.get()) + '.1')], context={})
pbeWithSHAAnd2_KeyTripleDES_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12PbeIds.get()) + '.4')], context={})
pbeWithSHAAnd3_KeyTripleDES_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12PbeIds.get()) + '.3')], context={})
pbeWithSHAAnd40BitRC4 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12PbeIds.get()) + '.2')], context={})
pbewithSHAAnd40BitRC2_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_12PbeIds.get()) + '.6')], context={})