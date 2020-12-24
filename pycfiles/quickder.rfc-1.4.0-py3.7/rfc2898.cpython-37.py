# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc2898.py
# Compiled at: 2020-03-04 06:24:39
# Size of source mod 2**32: 10298 bytes
import arpa2.quickder as _api

class AlgorithmIdentifier(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'algorithm':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'parameters':(
       '_TYPTR', ['_api.ASN1Any'], 1)})
    _context = globals()
    _numcursori = 2


class PBEParameter(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'salt':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'iterationCount':(
       '_TYPTR', ['_api.ASN1Integer'], 1)})
    _context = globals()
    _numcursori = 2


class PBES2_params(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'keyDerivationFunc':(
       '_TYPTR', ['AlgorithmIdentifier'], 0), 
      'encryptionScheme':(
       '_TYPTR', ['AlgorithmIdentifier'], 2)})
    _context = globals()
    _numcursori = 4


class PBKDF2_params(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'salt':(
       '_NAMED',
       {'specified':(
         '_TYPTR', ['_api.ASN1OctetString'], 0), 
        'otherSource':(
         '_TYPTR', ['AlgorithmIdentifier'], 1)}), 
      'iterationCount':(
       '_TYPTR', ['_api.ASN1Integer'], 3), 
      'keyLength':(
       '_TYPTR', ['_api.ASN1Integer'], 4), 
      'prf':(
       '_TYPTR', ['AlgorithmIdentifier'], 5)})
    _context = globals()
    _numcursori = 7


class PBKDF2Algorithms(_api.ASN1Any):
    _der_packer = chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Any'], 0)
    _context = globals()
    _numcursori = 1


class PBMAC1_params(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'keyDerivationFunc':(
       '_TYPTR', ['AlgorithmIdentifier'], 0), 
      'messageAuthScheme':(
       '_TYPTR', ['AlgorithmIdentifier'], 2)})
    _context = globals()
    _numcursori = 4


class RC2_CBC_Parameter(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'rc2ParameterVersion':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'iv':(
       '_TYPTR', ['_api.ASN1OctetString'], 1)})
    _context = globals()
    _numcursori = 2


class RC5_CBC_Parameters(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'version':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'rounds':(
       '_TYPTR', ['_api.ASN1Integer'], 1), 
      'blockSizeInBits':(
       '_TYPTR', ['_api.ASN1Integer'], 2), 
      'iv':(
       '_TYPTR', ['_api.ASN1OctetString'], 3)})
    _context = globals()
    _numcursori = 4


rsadsi = _api.ASN1OID(bindata=[_api.der_format_OID('1.2.840.113549')], context={})
encryptionAlgorithm = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(rsadsi.get()) + '.3')], context={})
des_EDE3_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(encryptionAlgorithm.get()) + '.7')], context={})
desCBC = _api.ASN1OID(bindata=[_api.der_format_OID('1.3.14.3.2.7')], context={})
digestAlgorithm = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(rsadsi.get()) + '.2')], context={})
pkcs = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(rsadsi.get()) + '.1')], context={})
pkcs_5 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs.get()) + '.5')], context={})
id_PBES2 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.13')], context={})
id_PBKDF2 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.12')], context={})
id_PBMAC1 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.14')], context={})
id_hmacWithSHA1 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(digestAlgorithm.get()) + '.7')], context={})
pbeWithMD2AndDES_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.1')], context={})
pbeWithMD2AndRC2_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.4')], context={})
pbeWithMD5AndDES_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.3')], context={})
pbeWithMD5AndRC2_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.6')], context={})
pbeWithSHA1AndDES_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.10')], context={})
pbeWithSHA1AndRC2_CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(pkcs_5.get()) + '.11')], context={})
rc2CBC = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(encryptionAlgorithm.get()) + '.2')], context={})
rc5_CBC_PAD = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(encryptionAlgorithm.get()) + '.9')], context={})