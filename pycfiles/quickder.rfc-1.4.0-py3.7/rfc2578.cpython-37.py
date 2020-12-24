# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quickder/rfc/rfc2578.py
# Compiled at: 2020-03-04 06:24:36
# Size of source mod 2**32: 9383 bytes
import arpa2.quickder as _api

class Counter64(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(6)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class IpAddress(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(0)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class TimeTicks(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(3)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class Opaque(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(4)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class Counter32(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class Unsigned32(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class ApplicationSyntax(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'ipAddress_value':(
       '_TYPTR', ['IpAddress'], 0), 
      'counter_value':(
       '_TYPTR', ['Counter32'], 1), 
      'timeticks_value':(
       '_TYPTR', ['TimeTicks'], 2), 
      'arbitrary_value':(
       '_TYPTR', ['Opaque'], 3), 
      'big_counter_value':(
       '_TYPTR', ['Counter64'], 4), 
      'unsigned_integer_value':(
       '_TYPTR', ['Unsigned32'], 5)})
    _context = globals()
    _numcursori = 6


class ExtUTCTime(_api.ASN1OctetString):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OctetString'], 0)
    _context = globals()
    _numcursori = 1


class Gauge32(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class Integer32(_api.ASN1Integer):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1Integer'], 0)
    _context = globals()
    _numcursori = 1


class NotificationName(_api.ASN1OID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OID'], 0)
    _context = globals()
    _numcursori = 1


class ObjectName(_api.ASN1OID):
    _der_packer = chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_END)
    _recipe = ('_TYPTR', ['_api.ASN1OID'], 0)
    _context = globals()
    _numcursori = 1


class SimpleSyntax(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'integer_value':(
       '_TYPTR', ['_api.ASN1Integer'], 0), 
      'string_value':(
       '_TYPTR', ['_api.ASN1OctetString'], 1), 
      'objectID_value':(
       '_TYPTR', ['_api.ASN1OID'], 2)})
    _context = globals()
    _numcursori = 3


class ObjectSyntax(_api.ASN1ConstructedType):
    _der_packer = chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_INTEGER) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OCTETSTRING) + chr(_api.DER_PACK_STORE | _api.DER_TAG_OBJECTIDENTIFIER) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_BEGIN) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(0)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(1)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(3)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(4)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(6)) + chr(_api.DER_PACK_STORE | _api.DER_TAG_APPLICATION(2)) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_CHOICE_END) + chr(_api.DER_PACK_END)
    _recipe = ('_NAMED',
     {'simple':(
       '_TYPTR', ['SimpleSyntax'], 0), 
      'application_wide':(
       '_TYPTR', ['ApplicationSyntax'], 3)})
    _context = globals()
    _numcursori = 9


org = _api.ASN1OID(bindata=[_api.der_format_OID('1.3')], context={})
dod = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(org.get()) + '.6')], context={})
internet = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(dod.get()) + '.1')], context={})
directory = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(internet.get()) + '.1')], context={})
private = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(internet.get()) + '.4')], context={})
enterprises = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(private.get()) + '.1')], context={})
experimental = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(internet.get()) + '.3')], context={})
mgmt = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(internet.get()) + '.2')], context={})
mib_2 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(mgmt.get()) + '.1')], context={})
security = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(internet.get()) + '.5')], context={})
snmpV2 = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(internet.get()) + '.6')], context={})
snmpDomains = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(snmpV2.get()) + '.1')], context={})
snmpModules = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(snmpV2.get()) + '.3')], context={})
snmpProxys = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(snmpV2.get()) + '.2')], context={})
transmission = _api.ASN1OID(bindata=[_api.der_format_OID(_api.der_parse_OID(mib_2.get()) + '.10')], context={})
zeroDotZero = _api.ASN1OID(bindata=[_api.der_format_OID('0.0')], context={})