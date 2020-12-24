# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc5208.py
# Compiled at: 2020-03-04 06:24:35
# Size of source mod 2**32: 6995 bytes
import arpa2.quickder as _api
from rfc2898 import AlgorithmIdentifier

class Context(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'contextType':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'contextValues':(
       '_SETOF', 1,
       chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['_api.ASN1Any'], 0)), 
      'fallback':(
       '_TYPTR', ['_api.ASN1Boolean'], 2)})
    _context = globals()
    _numcursori = 3


class Attribute(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'type':(
       '_TYPTR', ['_api.ASN1OID'], 0), 
      'values':(
       '_SETOF', 1,
       chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END), 1,
       (
        '_TYPTR', ['_api.ASN1Any'], 0)), 
      'valuesWithContext':(
       '_SETOF', 2,
       chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 2,
       (
        '_NAMED',
        {'value':(
          '_TYPTR', ['_api.ASN1Any'], 0), 
         'contextList':(
          '_SETOF', 1,
          chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
          (
           '_TYPTR', ['Context'], 0))}))})
    _context = globals()
    _numcursori = 3


class Attributes(_api.ASN1SetOf):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_END)
    _recipe = ('_SETOF', 0,
     chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_SET) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END), 3,
     (
      '_TYPTR', ['Attribute'], 0))
    _context = globals()
    _numcursori = 1


class EncryptedData(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class EncryptedPrivateKeyInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'encryptionAlgorithm':(
       '_TYPTR', ['AlgorithmIdentifier'], 0), 
      'encryptedData':(
       '_TYPTR', ['EncryptedData'], 2)})
    _context = globals()
    _numcursori = 3


class KeyEncryptionAlgorithms(_api.ASN1Any):
    _der_packer = chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Any'], 0)
    _context = globals()
    _numcursori = 1


class PrivateKey(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class PrivateKeyAlgorithms(_api.ASN1Any):
    _der_packer = chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Any'], 0)
    _context = globals()
    _numcursori = 1


class Version(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class PrivateKeyInfo(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_ANY) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'version':(
       '_TYPTR', ['Version'], 0), 
      'privateKeyAlgorithm':(
       '_TYPTR', ['AlgorithmIdentifier'], 1), 
      'privateKey':(
       '_TYPTR', ['PrivateKey'], 3), 
      'attributes':(
       '_TYPTR', ['Attributes'], 4)})
    _context = globals()
    _numcursori = 5