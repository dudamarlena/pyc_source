# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc3062.py
# Compiled at: 2020-03-04 06:24:44
# Size of source mod 2**32: 1998 bytes
import arpa2.quickder as _api

class PasswdModifyRequestValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(1)) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(2)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'userIdentity':(
       '_TYPTR', ['_api.ASN1OctetString'], 0), 
      'oldPasswd':(
       '_TYPTR', ['_api.ASN1OctetString'], 1), 
      'newPasswd':(
       '_TYPTR', ['_api.ASN1OctetString'], 2)})
    _context = globals()
    _numcursori = 3


class PasswdModifyResponseValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_CONTEXT(0)) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'genPasswd': ('_TYPTR', ['_api.ASN1OctetString'], 0)})
    _context = globals()
    _numcursori = 1


passwdModifyOID = _api.ASN1OID(bindata=[_api.der_format_OID('1.3.6.1.4.1.4203.1.11.1')], context={})