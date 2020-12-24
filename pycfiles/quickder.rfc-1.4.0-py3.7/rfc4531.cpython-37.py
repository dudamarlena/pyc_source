# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc4531.py
# Compiled at: 2020-03-04 06:24:41
# Size of source mod 2**32: 1024 bytes
import arpa2.quickder as _api
from rfc4511 import LDAPString

class TurnValue(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_ENTER | _api.DER_TAG_SEQUENCE) + chr(_api.DER_PACK_OPTIONAL) + chr(_api.DER_PACK_STORE | _api.DER_TAG_BOOLEAN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_LEAVE) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'mutual':(
       '_TYPTR', ['_api.ASN1Boolean'], 0), 
      'identifier':(
       '_TYPTR', ['LDAPString'], 1)})
    _context = globals()
    _numcursori = 2