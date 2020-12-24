# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc4120.py
# Compiled at: 2020-03-04 06:24:37
# Size of source mod 2**32: 113406 bytes
import arpa2.quickder as _api

class Int32(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class AuthorizationData(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_NAMED',
      {'ad_type':(
        '_TYPTR', ['Int32'], 0), 
       'ad_data':(
        '_TYPTR', ['_api.ASN1OctetString'], 1)}))
    _context = globals()
    _numcursori = 1


class AD_AND_OR(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'condition_count':(
       '_TYPTR', ['Int32'], 0), 
      'elements':(
       '_TYPTR', ['AuthorizationData'], 1)})
    _context = globals()
    _numcursori = 2


class AD_IF_RELEVANT(AuthorizationData):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['AuthorizationData'], 0)
    _context = globals()
    _numcursori = 1


class Checksum(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'cksumtype':(
       '_TYPTR', ['Int32'], 0), 
      'checksum':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class KerberosString(_api.ASN1GeneralString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1GeneralString'], 0)
    _context = globals()
    _numcursori = 1


class PrincipalName(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'name_type':(
       '_TYPTR', ['Int32'], 0), 
      'name_string':(
       '_SEQOF', 1,
       chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['KerberosString'], 0))})
    _context = globals()
    _numcursori = 2


class Realm(KerberosString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KerberosString'], 0)
    _context = globals()
    _numcursori = 1


class AD_KDCIssued(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'ad_checksum':(
       '_TYPTR', ['Checksum'], 0), 
      'i_realm':(
       '_TYPTR', ['Realm'], 2), 
      'i_sname':(
       '_TYPTR', ['PrincipalName'], 3), 
      'elements':(
       '_TYPTR', ['AuthorizationData'], 5)})
    _context = globals()
    _numcursori = 6


class AD_MANDATORY_FOR_KDC(AuthorizationData):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['AuthorizationData'], 0)
    _context = globals()
    _numcursori = 1


class UInt32(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class EncryptedData(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'etype':(
       '_TYPTR', ['Int32'], 0), 
      'kvno':(
       '_TYPTR', ['UInt32'], 1), 
      'cipher':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class AP_REP(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(15)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'enc_part':(
       '_TYPTR', ['EncryptedData'], 2)})
    _context = globals()
    _numcursori = 5


class KerberosFlags(_api.ASN1BitString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1BitString'], 0)
    _context = globals()
    _numcursori = 1


class APOptions(KerberosFlags):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KerberosFlags'], 0)
    _context = globals()
    _numcursori = 1


class Ticket(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'tkt_vno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'realm':(
       '_TYPTR', ['Realm'], 1), 
      'sname':(
       '_TYPTR', ['PrincipalName'], 2), 
      'enc_part':(
       '_TYPTR', ['EncryptedData'], 4)})
    _context = globals()
    _numcursori = 7


class AP_REQ(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(14)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'ap_options':(
       '_TYPTR', ['APOptions'], 2), 
      'ticket':(
       '_TYPTR', ['Ticket'], 3), 
      'authenticator':(
       '_TYPTR', ['EncryptedData'], 10)})
    _context = globals()
    _numcursori = 13


class PA_DATA(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'padata_type':(
       '_TYPTR', ['Int32'], 0), 
      'padata_value':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class KDC_REP(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'padata':(
       '_SEQOF', 2,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_TYPTR', ['PA-DATA'], 0)), 
      'crealm':(
       '_TYPTR', ['Realm'], 3), 
      'cname':(
       '_TYPTR', ['PrincipalName'], 4), 
      'ticket':(
       '_TYPTR', ['Ticket'], 6), 
      'enc_part':(
       '_TYPTR', ['EncryptedData'], 13)})
    _context = globals()
    _numcursori = 16


class AS_REP(KDC_REP):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(11)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KDC-REP'], 0)
    _context = globals()
    _numcursori = 16


class KDCOptions(KerberosFlags):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KerberosFlags'], 0)
    _context = globals()
    _numcursori = 1


class KerberosTime(_api.ASN1GeneralizedTime):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1GeneralizedTime'], 0)
    _context = globals()
    _numcursori = 1


class HostAddress(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'addr_type':(
       '_TYPTR', ['Int32'], 0), 
      'address':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class HostAddresses(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['HostAddress'], 0))
    _context = globals()
    _numcursori = 1


class KDC_REQ_BODY(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'kdc_options':(
       '_TYPTR', ['KDCOptions'], 0), 
      'cname':(
       '_TYPTR', ['PrincipalName'], 1), 
      'realm':(
       '_TYPTR', ['Realm'], 3), 
      'sname':(
       '_TYPTR', ['PrincipalName'], 4), 
      'from':(
       '_TYPTR', ['KerberosTime'], 6), 
      'till':(
       '_TYPTR', ['KerberosTime'], 7), 
      'rtime':(
       '_TYPTR', ['KerberosTime'], 8), 
      'nonce':(
       '_TYPTR', ['UInt32'], 9), 
      'etype':(
       '_SEQOF', 10,
       chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['Int32'], 0)), 
      'addresses':(
       '_TYPTR', ['HostAddresses'], 11), 
      'enc_authorization_data':(
       '_TYPTR', ['EncryptedData'], 12), 
      'additional_tickets':(
       '_SEQOF', 15,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 7,
       (
        '_TYPTR', ['Ticket'], 0))})
    _context = globals()
    _numcursori = 16


class KDC_REQ(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'padata':(
       '_SEQOF', 2,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_TYPTR', ['PA-DATA'], 0)), 
      'req_body':(
       '_TYPTR', ['KDC-REQ-BODY'], 3)})
    _context = globals()
    _numcursori = 19


class AS_REQ(KDC_REQ):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KDC-REQ'], 0)
    _context = globals()
    _numcursori = 19


class Microseconds(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class EncryptionKey(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'keytype':(
       '_TYPTR', ['Int32'], 0), 
      'keyvalue':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class Authenticator(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'authenticator_vno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'crealm':(
       '_TYPTR', ['Realm'], 1), 
      'cname':(
       '_TYPTR', ['PrincipalName'], 2), 
      'cksum':(
       '_TYPTR', ['Checksum'], 4), 
      'cusec':(
       '_TYPTR', ['Microseconds'], 6), 
      'ctime':(
       '_TYPTR', ['KerberosTime'], 7), 
      'subkey':(
       '_TYPTR', ['EncryptionKey'], 8), 
      'seq_number':(
       '_TYPTR', ['UInt32'], 10), 
      'authorization_data':(
       '_TYPTR', ['AuthorizationData'], 11)})
    _context = globals()
    _numcursori = 12


class ETYPE_INFO_ENTRY(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'etype':(
       '_TYPTR', ['Int32'], 0), 
      'salt':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class ETYPE_INFO(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['ETYPE-INFO-ENTRY'], 0))
    _context = globals()
    _numcursori = 1


class ETYPE_INFO2_ENTRY(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'etype':(
       '_TYPTR', ['Int32'], 0), 
      'salt':(
       '_TYPTR', ['KerberosString'], 1), 
      's2kparams':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class ETYPE_INFO2(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['ETYPE-INFO2-ENTRY'], 0))
    _context = globals()
    _numcursori = 1


class EncAPRepPart(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(27)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'ctime':(
       '_TYPTR', ['KerberosTime'], 0), 
      'cusec':(
       '_TYPTR', ['Microseconds'], 1), 
      'subkey':(
       '_TYPTR', ['EncryptionKey'], 2), 
      'seq_number':(
       '_TYPTR', ['UInt32'], 4)})
    _context = globals()
    _numcursori = 5


class LastReq(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_NAMED',
      {'lr_type':(
        '_TYPTR', ['Int32'], 0), 
       'lr_value':(
        '_TYPTR', ['KerberosTime'], 1)}))
    _context = globals()
    _numcursori = 1


class TicketFlags(KerberosFlags):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KerberosFlags'], 0)
    _context = globals()
    _numcursori = 1


class EncKDCRepPart(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'key':(
       '_TYPTR', ['EncryptionKey'], 0), 
      'last_req':(
       '_TYPTR', ['LastReq'], 2), 
      'nonce':(
       '_TYPTR', ['UInt32'], 3), 
      'key_expiration':(
       '_TYPTR', ['KerberosTime'], 4), 
      'flags':(
       '_TYPTR', ['TicketFlags'], 5), 
      'authtime':(
       '_TYPTR', ['KerberosTime'], 6), 
      'starttime':(
       '_TYPTR', ['KerberosTime'], 7), 
      'endtime':(
       '_TYPTR', ['KerberosTime'], 8), 
      'renew_till':(
       '_TYPTR', ['KerberosTime'], 9), 
      'srealm':(
       '_TYPTR', ['Realm'], 10), 
      'sname':(
       '_TYPTR', ['PrincipalName'], 11), 
      'caddr':(
       '_TYPTR', ['HostAddresses'], 13)})
    _context = globals()
    _numcursori = 14


class EncASRepPart(EncKDCRepPart):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(25)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['EncKDCRepPart'], 0)
    _context = globals()
    _numcursori = 14


class KrbCredInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'key':(
       '_TYPTR', ['EncryptionKey'], 0), 
      'prealm':(
       '_TYPTR', ['Realm'], 2), 
      'pname':(
       '_TYPTR', ['PrincipalName'], 3), 
      'flags':(
       '_TYPTR', ['TicketFlags'], 5), 
      'authtime':(
       '_TYPTR', ['KerberosTime'], 6), 
      'starttime':(
       '_TYPTR', ['KerberosTime'], 7), 
      'endtime':(
       '_TYPTR', ['KerberosTime'], 8), 
      'renew_till':(
       '_TYPTR', ['KerberosTime'], 9), 
      'srealm':(
       '_TYPTR', ['Realm'], 10), 
      'sname':(
       '_TYPTR', ['PrincipalName'], 11), 
      'caddr':(
       '_TYPTR', ['HostAddresses'], 13)})
    _context = globals()
    _numcursori = 14


class EncKrbCredPart(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(29)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'ticket_info':(
       '_SEQOF', 0,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 14,
       (
        '_TYPTR', ['KrbCredInfo'], 0)), 
      'nonce':(
       '_TYPTR', ['UInt32'], 1), 
      'timestamp':(
       '_TYPTR', ['KerberosTime'], 2), 
      'usec':(
       '_TYPTR', ['Microseconds'], 3), 
      's_address':(
       '_TYPTR', ['HostAddress'], 4), 
      'r_address':(
       '_TYPTR', ['HostAddress'], 6)})
    _context = globals()
    _numcursori = 8


class EncKrbPrivPart(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(28)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'user_data':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'timestamp':(
       '_TYPTR', ['KerberosTime'], 1), 
      'usec':(
       '_TYPTR', ['Microseconds'], 2), 
      'seq_number':(
       '_TYPTR', ['UInt32'], 3), 
      's_address':(
       '_TYPTR', ['HostAddress'], 4), 
      'r_address':(
       '_TYPTR', ['HostAddress'], 6)})
    _context = globals()
    _numcursori = 8


class EncTGSRepPart(EncKDCRepPart):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(26)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['EncKDCRepPart'], 0)
    _context = globals()
    _numcursori = 14


class TransitedEncoding(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'tr_type':(
       '_TYPTR', ['Int32'], 0), 
      'contents':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class EncTicketPart(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'flags':(
       '_TYPTR', ['TicketFlags'], 0), 
      'key':(
       '_TYPTR', ['EncryptionKey'], 1), 
      'crealm':(
       '_TYPTR', ['Realm'], 3), 
      'cname':(
       '_TYPTR', ['PrincipalName'], 4), 
      'transited':(
       '_TYPTR', ['TransitedEncoding'], 6), 
      'authtime':(
       '_TYPTR', ['KerberosTime'], 8), 
      'starttime':(
       '_TYPTR', ['KerberosTime'], 9), 
      'endtime':(
       '_TYPTR', ['KerberosTime'], 10), 
      'renew_till':(
       '_TYPTR', ['KerberosTime'], 11), 
      'caddr':(
       '_TYPTR', ['HostAddresses'], 12), 
      'authorization_data':(
       '_TYPTR', ['AuthorizationData'], 13)})
    _context = globals()
    _numcursori = 14


class KRB_CRED(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(22)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'tickets':(
       '_SEQOF', 2,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 7,
       (
        '_TYPTR', ['Ticket'], 0)), 
      'enc_part':(
       '_TYPTR', ['EncryptedData'], 3)})
    _context = globals()
    _numcursori = 6


class KRB_ERROR(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(30)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(12)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'ctime':(
       '_TYPTR', ['KerberosTime'], 2), 
      'cusec':(
       '_TYPTR', ['Microseconds'], 3), 
      'stime':(
       '_TYPTR', ['KerberosTime'], 4), 
      'susec':(
       '_TYPTR', ['Microseconds'], 5), 
      'error_code':(
       '_TYPTR', ['Int32'], 6), 
      'crealm':(
       '_TYPTR', ['Realm'], 7), 
      'cname':(
       '_TYPTR', ['PrincipalName'], 8), 
      'realm':(
       '_TYPTR', ['Realm'], 10), 
      'sname':(
       '_TYPTR', ['PrincipalName'], 11), 
      'e_text':(
       '_TYPTR', ['KerberosString'], 13), 
      'e_data':(
       '_TYPTR', ['_api.ASN1OctetString'], 14)})
    _context = globals()
    _numcursori = 15


class KRB_PRIV(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(21)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'enc_part':(
       '_TYPTR', ['EncryptedData'], 2)})
    _context = globals()
    _numcursori = 5


class KRB_SAFE_BODY(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'user_data':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'timestamp':(
       '_TYPTR', ['KerberosTime'], 1), 
      'usec':(
       '_TYPTR', ['Microseconds'], 2), 
      'seq_number':(
       '_TYPTR', ['UInt32'], 3), 
      's_address':(
       '_TYPTR', ['HostAddress'], 4), 
      'r_address':(
       '_TYPTR', ['HostAddress'], 6)})
    _context = globals()
    _numcursori = 8


class KRB_SAFE(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(20)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'pvno':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'msg_type':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'safe_body':(
       '_TYPTR', ['KRB-SAFE-BODY'], 2), 
      'cksum':(
       '_TYPTR', ['Checksum'], 10)})
    _context = globals()
    _numcursori = 12


class METHOD_DATA(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_TYPTR', ['PA-DATA'], 0))
    _context = globals()
    _numcursori = 1


class PA_ENC_TIMESTAMP(EncryptedData):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['EncryptedData'], 0)
    _context = globals()
    _numcursori = 3


class PA_ENC_TS_ENC(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'patimestamp':(
       '_TYPTR', ['KerberosTime'], 0), 
      'pausec':(
       '_TYPTR', ['Microseconds'], 1)})
    _context = globals()
    _numcursori = 2


class TGS_REP(KDC_REP):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(13)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KDC-REP'], 0)
    _context = globals()
    _numcursori = 16


class TGS_REQ(KDC_REQ):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_APPLICATION(12)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BITSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(3)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(5)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_GENERALIZEDTIME) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(7)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(8)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(9)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(10)) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(11)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['KDC-REQ'], 0)
    _context = globals()
    _numcursori = 19


class TYPED_DATA(_api.ASN1SequenceOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_END)
    _recipe = ('_SEQOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
     (
      '_NAMED',
      {'data_type':(
        '_TYPTR', ['Int32'], 0), 
       'data_value':(
        '_TYPTR', ['_api.ASN1OctetString'], 1)}))
    _context = globals()
    _numcursori = 1


id_krb5 = _api.ASN1OID(bindata=[_api.der_format_OID('1.3.6.1.5.2')], context={})