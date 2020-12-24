# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\microsoft.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
import ctypes
from pyasn1.type.namedtype import NamedTypes, NamedType
from pyasn1.type.tag import Tag, tagClassApplication, tagFormatConstructed
from pyasn1.type.univ import Sequence, OctetString, Integer
from .rfc4511 import ResultCode, LDAPString
from .controls import build_control

class SicilyBindResponse(Sequence):
    tagSet = Sequence.tagSet.tagImplicitly(Tag(tagClassApplication, tagFormatConstructed, 1))
    componentType = NamedTypes(NamedType('resultCode', ResultCode()), NamedType('serverCreds', OctetString()), NamedType('errorMessage', LDAPString()))


class DirSyncControlRequestValue(Sequence):
    componentType = NamedTypes(NamedType('Flags', Integer()), NamedType('MaxBytes', Integer()), NamedType('Cookie', OctetString()))


class DirSyncControlResponseValue(Sequence):
    componentType = NamedTypes(NamedType('MoreResults', Integer()), NamedType('unused', Integer()), NamedType('CookieServer', OctetString()))


class SdFlags(Sequence):
    componentType = NamedTypes(NamedType('Flags', Integer()))


class ExtendedDN(Sequence):
    componentType = NamedTypes(NamedType('option', Integer()))


def dir_sync_control(criticality, object_security, ancestors_first, public_data_only, incremental_values, max_length, cookie):
    control_value = DirSyncControlRequestValue()
    flags = 0
    if object_security:
        flags |= 1
    if ancestors_first:
        flags |= 2048
    if public_data_only:
        flags |= 8192
    if incremental_values:
        flags |= 2147483648
        flags = ctypes.c_long(flags & 4294967295).value
    control_value.setComponentByName('Flags', flags)
    control_value.setComponentByName('MaxBytes', max_length)
    if cookie:
        control_value.setComponentByName('Cookie', cookie)
    else:
        control_value.setComponentByName('Cookie', OctetString(''))
    return build_control('1.2.840.113556.1.4.841', criticality, control_value)


def extended_dn_control(criticality=False, hex_format=False):
    control_value = ExtendedDN()
    control_value.setComponentByName('option', Integer(not hex_format))
    return build_control('1.2.840.113556.1.4.529', criticality, control_value)


def show_deleted_control(criticality=False):
    return build_control('1.2.840.113556.1.4.417', criticality, value=None)


def security_descriptor_control(criticality=False, sdflags=15):
    sdcontrol = SdFlags()
    sdcontrol.setComponentByName('Flags', sdflags)
    return [build_control('1.2.840.113556.1.4.801', criticality, sdcontrol)]