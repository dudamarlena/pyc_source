# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/sd.py
# Compiled at: 2014-07-11 17:28:33
import struct, bta.tools.decoding
from bta.tools.flags import Flags, Enums

class SE:
    SE_OWNER_DEFAULTED = 1
    SE_GROUP_DEFAULTED = 2
    SE_DACL_PRESENT = 4
    SE_DACL_DEFAULTED = 8
    SE_SACL_PRESENT = 16
    SE_SACL_DEFAULTED = 32
    SE_DACL_AUTO_INHERIT_REQ = 256
    SE_SACL_AUTO_INHERIT_REQ = 512
    SE_DACL_AUTO_INHERITED = 1024
    SE_SACL_AUTO_INHERITED = 2048
    SE_DACL_PROTECTED = 4096
    SE_SACL_PROTECTED = 8192
    SE_SELF_RELATIVE = 32768


class SecurityDescriptor(object):

    def __init__(self, sd):
        self.raw_sd = sd
        _rev, _sbz, ctrl, owner, group, sacl, dacl = struct.unpack_from('<BBHIIII', sd)
        self.ctrl = ctrl
        self.owner = owner
        self.group = group
        if self.ctrl & SE.SE_SELF_RELATIVE:
            if self.ctrl & SE.SE_SACL_PRESENT:
                self.sacl = sd[sacl:dacl]
            if self.ctrl & SE.SE_DACL_PRESENT:
                self.dacl = sd[dacl:]


class ACL(object):

    def __init__(self, acl):
        _rev, _sbz, _sz, _count, _sbz2 = struct.unpack_from('<BBHHH', acl)


class ACE(object):

    def __init__(self, ace):
        _type, _flags, _size = struct.unpack_from('<BBH', ace)


class ACEType(Enums):
    _enum_ = {'AccessAllowed': 0, 
       'AccessDenied': 1, 
       'SystemAudit': 2, 
       'SystemAlarm': 3, 
       'AccessAllowedCompound': 4, 
       'AccessAllowedObject': 5, 
       'AccessDeniedObject': 6, 
       'SystemAuditObject': 7, 
       'SystemAlarmObject': 8}


class SidTypeName(Enums):
    _enum_ = {'User': 1, 
       'Domain': 2, 
       'Alias': 3, 
       'WellKnownGroup': 4, 
       'DeletedAccount': 5, 
       'Invalid': 6, 
       'Unknown': 7, 
       'Computer': 8}


class ControlFlags(Flags):
    _flags_ = {'OwnerDefaulted': 1, 
       'GroupDefaulted': 2, 
       'DACLPresent': 4, 
       'DACLDefaulted': 8, 
       'SACLPresent': 16, 
       'SACLDefaulted': 32, 
       'DACLAutoInheritReq': 256, 
       'SACLAutoInheritReq': 512, 
       'DACLAutoInherited': 1024, 
       'SACLAutoInherited': 2048, 
       'DACLProtected': 4096, 
       'SACLProtected': 8192, 
       'SelfRelative': 32768}


class ACEFlags(Flags):
    _flags_ = {'ObjectInheritAce': 1, 
       'ContainerInheritAce': 2, 
       'NoPropagateInheritAce': 4, 
       'InheritOnlyAce': 8, 
       'InheritedAce': 16, 
       'SuccessfulAccessAceFlag': 64, 
       'FailedAccessAceFlag': 128}


class ACEObjectFlags(Flags):
    _flags_ = {'ObjectTypePresent': 1, 
       'InheritedObjectTypePresent': 2}


class AccessMask(Flags):
    _flags_ = {'GenericRead': 2147483648, 
       'GenericWrite': 1073741824, 
       'GenericExecute': 536870912, 
       'GenericAll': 268435456, 
       'AcessSystemAcl': 16777216, 
       'Delete': 65536, 
       'ReadControl': 131072, 
       'WriteDAC': 262144, 
       'WriteOwner': 524288, 
       'Synchronize': 1048576, 
       'AccessSystemSecurity': 16777216, 
       'MaximumAllowed': 33554432, 
       'StandardsRightsRequired': 983040, 
       'StandarRightsAll': 2031616, 
       'SpecificRightsAll': 65535, 
       'ADSRightDSCreateChild': 1, 
       'ADSRightDSDeleteChild': 2, 
       'ADSRightACTRLDSList': 4, 
       'ADSRightDSSelf': 8, 
       'ADSRightDSReadProp': 16, 
       'ADSRightDSWriteProp': 32, 
       'ADSRightDSDeleteTree': 64, 
       'ADSRightDSListObject': 128, 
       'ADSRightDSControlAccess': 256}


def acl_to_json(acl):
    rev, _sbz, size, count, _sbz2 = struct.unpack_from('<BBHHH', acl)
    ACL = {}
    ACL['Revision'] = rev
    ACL['Size'] = size
    ACL['Count'] = count
    ACL['ACEList'] = ACEList = []
    acestr = acl[8:]
    while count > 0:
        typeraw, flags, size = struct.unpack_from('<BBH', acestr)
        type_ = ACEType(typeraw)
        ACE = {}
        ACE['Type'] = type_.to_json()
        ACE['Flags'] = ACEFlags(flags).to_json()
        ACE['Size'] = size
        amask, = struct.unpack_from('<I', acestr[4:])
        ACE['AccessMask'] = AccessMask(amask).to_json()
        sstr = acestr[8:size]
        if typeraw in (5, 6, 7, 8):
            objflagsraw, = struct.unpack_from('<I', sstr)
            sstr = sstr[4:]
            objflags = ACEObjectFlags(objflagsraw)
            ACE['ObjectFlags'] = objflags.to_json()
            if objflags.ObjectTypePresent:
                ACE['ObjectType'] = bta.tools.decoding.decode_guid(sstr[:16])
                sstr = sstr[16:]
            if objflags.InheritedObjectTypePresent:
                ACE['InheritedObjectType'] = bta.tools.decoding.decode_guid(sstr[:16])
                sstr = sstr[16:]
        if typeraw in (0, 1, 2, 3, 5, 6, 7, 8):
            ACE['SID'] = bta.tools.decoding.decode_sid(sstr)
        if type == 0:
            pass
        elif type == 1:
            pass
        elif type == 2:
            pass
        elif type == 3:
            pass
        elif type == 4:
            pass
        elif type == 5:
            pass
        elif type == 6:
            pass
        elif type == 7:
            pass
        elif type == 8:
            pass
        ACEList.append(ACE)
        acestr = acestr[size:]
        count -= 1

    return ACL


def sd_to_json(sd):
    jsd = {}
    rev, _sbz, rctrl, owner, group, saclofs, daclofs = struct.unpack_from('<BBHIIII', sd)
    ctrl = ControlFlags(rctrl)
    jsd['Revision'] = rev
    jsd['Control'] = ctrl.to_json()
    if ctrl.SelfRelative:
        jsd['Owner'] = bta.tools.decoding.decode_sid(sd[owner:])
        jsd['Group'] = bta.tools.decoding.decode_sid(sd[group:])
        if ctrl.SACLPresent:
            jsd['SACL'] = acl_to_json(sd[saclofs:])
        if ctrl.DACLPresent:
            jsd['DACL'] = acl_to_json(sd[daclofs:])
    return jsd


if __name__ == '__main__':
    from pprint import pprint
    for sd in []:
        pprint(sd_to_json(sd.strip().decode('hex')))