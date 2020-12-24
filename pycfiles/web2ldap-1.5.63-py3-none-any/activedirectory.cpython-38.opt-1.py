# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/activedirectory.py
# Compiled at: 2019-12-16 13:32:28
# Size of source mod 2**32: 29308 bytes
"""
web2ldap plugin classes for Active Directory (for some information see draft-armijo-ldap-syntax)
"""
import os, time, struct, uuid
from ldap0.dn import is_dn
from ldap0.msad import sid2sddl, sddl2sid
import web2ldapcnf, web2ldap.web, web2ldap.app.searchform
from web2ldap.utctime import strftimeiso8601
from web2ldap.app.plugins.groups import GroupEntryDN
from web2ldap.app.schema.syntaxes import Binary, BitArrayInteger, Boolean, DirectoryString, DistinguishedName, DNSDomain, DynamicDNSelectList, DynamicValueSelectList, GeneralizedTime, IA5String, Integer, OctetString, OID, PropertiesSelectList, SelectList, Uri, XmlValue, syntax_registry

class ObjectCategory(DynamicDNSelectList, DistinguishedName):
    oid = 'ObjectCategory-oid'
    oid: str
    desc = 'DN of the class entry'
    desc: str
    ldap_url = 'ldap:///CN=Schema,CN=Configuration,_?cn?one?(objectClass=classSchema)'
    ref_attrs = ((None, 'Same category', None, None), )


syntax_registry.reg_at(ObjectCategory.oid, [
 '1.2.840.113556.1.4.782',
 '1.2.840.113556.1.4.783'])

class ObjectVersion(Integer, SelectList):
    oid = 'ObjectVersion-oid'
    oid: str
    desc = 'Object version in MS AD (see [MS-ADTS])'
    desc: str
    attr_value_dict = {'13':'Windows 2000 Server operating system',  '30':'\uf020Windows Server 2003 operating system or Windows Server 2008 (AD LDS)', 
     '31':'Windows Server 2003 R2 operating system or Windows Server 2008 R2 (AD LDS)', 
     '44':'Windows Server 2008 operating system (AD DS)', 
     '47':'Windows Server 2008 R2 (AD DS)', 
     '11221':'Exchange 2007 SP1', 
     '11222':'Exchange 2007 SP2', 
     '12639':'Exchange 2010', 
     '12640':'Exchange 2010', 
     '13040':'Exchange 2010 SP1', 
     '13214':'Exchange 2010 SP1', 
     '14247':'Exchange 2010 SP2'}

    def display(self, valueindex=0, commandbutton=False) -> str:
        return SelectList.display(self, valueindex, commandbutton)


syntax_registry.reg_at(ObjectVersion.oid, [
 '1.2.840.113556.1.2.76'])

class ObjectSID(OctetString, IA5String):
    oid = 'ObjectSID-oid'
    oid: str
    desc = 'Base class for Windows Security Identifiers'
    desc: str

    def _validate(self, attrValue: bytes) -> bool:
        return OctetString._validate(self, attrValue)

    def sanitize(self, attrValue: bytes) -> bytes:
        if not attrValue:
            return b''
        return sddl2sid(attrValue.decode('ascii'))

    def formValue(self) -> str:
        if not self._av:
            return ''
        return sid2sddl(self._av)

    def formField(self) -> str:
        return IA5String.formField(self)

    def display(self, valueindex=0, commandbutton=False) -> str:
        return '%s<br>%s' % (
         self._app.form.utf2display(sid2sddl(self._av)),
         OctetString.display(self, valueindex, commandbutton))


syntax_registry.reg_at(ObjectSID.oid, [
 '1.2.840.113556.1.4.146',
 '1.2.840.113556.1.4.609'])

class OtherSID(ObjectSID):
    oid = 'OtherSID-oid'
    oid: str
    desc = 'SID in MS AD which points to another object'
    desc: str
    editable = False
    editable: bool
    well_known_sids = {'S-1-0-0':'NULL', 
     'S-1-1':'WORLD_DOMAIN', 
     'S-1-1-0':'WORLD', 
     'S-1-3':'CREATOR_OWNER_DOMAIN', 
     'S-1-3-0':'CREATOR_OWNER', 
     'S-1-3-1':'CREATOR_GROUP', 
     'S-1-3-4':'OWNER_RIGHTS', 
     'S-1-5':'NT_AUTHORITY', 
     'S-1-5-1':'NT_DIALUP', 
     'S-1-5-2':'NT_NETWORK', 
     'S-1-5-3':'NT_BATCH', 
     'S-1-5-4':'NT_INTERACTIVE', 
     'S-1-5-6':'NT_SERVICE', 
     'S-1-5-7':'NT_ANONYMOUS', 
     'S-1-5-8':'NT_PROXY', 
     'S-1-5-9':'NT_ENTERPRISE_DCS', 
     'S-1-5-10':'NT_SELF', 
     'S-1-5-11':'NT_AUTHENTICATED_USERS', 
     'S-1-5-12':'NT_RESTRICTED', 
     'S-1-5-13':'NT_TERMINAL_SERVER_USERS', 
     'S-1-5-14':'NT_REMOTE_INTERACTIVE', 
     'S-1-5-15':'NT_THIS_ORGANISATION', 
     'S-1-5-17':'NT_IUSR', 
     'S-1-5-18':'NT_SYSTEM', 
     'S-1-5-19':'NT_LOCAL_SERVICE', 
     'S-1-5-20':'NT_NETWORK_SERVICE', 
     'S-1-5-64-21':'NT_DIGEST_AUTHENTICATION', 
     'S-1-5-64-10':'NT_NTLM_AUTHENTICATION', 
     'S-1-5-64-14':'NT_SCHANNEL_AUTHENTICATION', 
     'S-1-5-1000':'NT_OTHER_ORGANISATION', 
     'S-1-5-32':'BUILTIN', 
     'S-1-5-32-544':'BUILTIN_ADMINISTRATORS', 
     'S-1-5-32-545':'BUILTIN_USERS', 
     'S-1-5-32-546':'BUILTIN_GUESTS', 
     'S-1-5-32-547':'BUILTIN_POWER_USERS', 
     'S-1-5-32-548':'BUILTIN_ACCOUNT_OPERATORS', 
     'S-1-5-32-549':'BUILTIN_SERVER_OPERATORS', 
     'S-1-5-32-550':'BUILTIN_PRINT_OPERATORS', 
     'S-1-5-32-551':'BUILTIN_BACKUP_OPERATORS', 
     'S-1-5-32-552':'BUILTIN_REPLICATOR', 
     'S-1-5-32-553':'BUILTIN_RAS_SERVERS', 
     'S-1-5-32-554':'BUILTIN_PREW2K', 
     'S-1-5-32-555':'BUILTIN_REMOTE_DESKTOP_USERS', 
     'S-1-5-32-556':'BUILTIN_NETWORK_CONF_OPERATORS'}

    def display(self, valueindex=0, commandbutton=False) -> str:
        sddl_str = sid2sddl(self._av)
        search_anchor = self.well_known_sids.get(sddl_str, '')
        if commandbutton:
            if sddl_str not in self.well_known_sids:
                search_anchor = self._app.anchor('searchform',
                  '&raquo;', [
                 (
                  'dn', self._dn),
                 ('searchform_mode', 'adv'),
                 ('search_attr', 'objectSid'),
                 (
                  'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                 (
                  'search_string', sddl_str)],
                  title='Search by SID')
        return '%s %s<br>%s' % (
         self._app.form.utf2display(sddl_str),
         search_anchor,
         OctetString.display(self, valueindex, commandbutton))


syntax_registry.reg_at(OtherSID.oid, [
 '1.2.840.113556.1.4.1301',
 '1.2.840.113556.1.4.1418',
 '1.2.840.113556.1.4.1303',
 '1.2.840.113556.1.4.667',
 '1.2.840.113556.1.4.1410'])

class SAMAccountName(DirectoryString):
    oid = 'SAMAccountName-oid'
    oid: str
    desc = 'SAM-Account-Name in MS AD'
    desc: str
    maxLen = 20
    maxLen: int


syntax_registry.reg_at(SAMAccountName.oid, [
 '1.2.840.113556.1.4.221'])

class SAMAccountType(SelectList):
    __doc__ = '\n    http://msdn.microsoft.com/library/default.asp?url=/library/en-us/adschema/adschema/a_samaccounttype.asp\n    '
    oid = 'SAMAccountType-oid'
    oid: str
    desc = 'SAM-Account-Type in MS AD'
    desc: str
    attr_value_dict = {'268435456':'SAM_GROUP_OBJECT',  '268435457':'SAM_NON_SECURITY_GROUP_OBJECT', 
     '536870912':'SAM_ALIAS_OBJECT', 
     '536870913':'SAM_NON_SECURITY_ALIAS_OBJECT', 
     '805306368':'SAM_NORMAL_USER_ACCOUNT', 
     '805306369':'SAM_MACHINE_ACCOUNT', 
     '805306370':'SAM_TRUST_ACCOUNT', 
     '1073741824':'SAM_APP_BASIC_GROUP', 
     '1073741825':'SAM_APP_QUERY_GROUP', 
     '2147483647':'SAM_ACCOUNT_TYPE_MAX'}


syntax_registry.reg_at(SAMAccountType.oid, [
 '1.2.840.113556.1.4.302'])

class GroupType(BitArrayInteger):
    __doc__ = '\n    http://msdn.microsoft.com/library/default.asp?url=/library/en-us/adschema/adschema/a_samaccounttype.asp\n    '
    oid = 'GroupType-oid'
    oid: str
    desc = 'Group-Type in MS AD'
    desc: str
    flag_desc_table = (('Group created by system', 1), ('Group with global scope', 2),
                       ('Group with domain local scope', 4), ('Group with universal scope', 8),
                       ('APP_BASIC group Authz Mgr', 16), ('APP_QUERY group Authz Mgr.', 32),
                       ('Security group', 2147483648))


syntax_registry.reg_at(GroupType.oid, [
 '1.2.840.113556.1.4.750'])

class DomainRID(SelectList):
    oid = 'DomainRID-oid'
    oid: str
    desc = 'Domain RID in MS AD'
    desc: str
    attr_value_dict = {'9':'DOMAIN_RID_LOGON',  '500':'DOMAIN_RID_ADMINISTRATOR', 
     '501':'DOMAIN_RID_GUEST', 
     '502':'DOMAIN_RID_KRBTGT', 
     '512':'DOMAIN_RID_ADMINS', 
     '513':'DOMAIN_RID_USERS', 
     '514':'DOMAIN_RID_GUESTS', 
     '515':'DOMAIN_RID_DOMAIN_MEMBERS', 
     '516':'DOMAIN_RID_DCS', 
     '517':'DOMAIN_RID_CERT_ADMINS', 
     '518':'DOMAIN_RID_SCHEMA_ADMINS', 
     '519':'DOMAIN_RID_ENTERPRISE_ADMINS', 
     '520':'DOMAIN_RID_POLICY_ADMINS'}


syntax_registry.reg_at(DomainRID.oid, [
 '1.2.840.113556.1.4.98'])

class UserAccountControl(BitArrayInteger):
    __doc__ = '\n    See knowledge base article 305144:\n    http://support.microsoft.com/default.aspx?scid=kb;en-us;Q305144\n    '
    oid = 'UserAccountControl-oid'
    oid: str
    flag_desc_table = (('SCRIPT', 1), ('ACCOUNTDISABLE', 2), ('HOMEDIR_REQUIRED', 8),
                       ('LOCKOUT', 16), ('PASSWD_NOTREQD', 32), ('PASSWD_CANT_CHANGE', 64),
                       ('ENCRYPTED_TEXT_PWD_ALLOWED', 128), ('TEMP_DUPLICATE_ACCOUNT', 256),
                       ('NORMAL_ACCOUNT', 512), ('INTERDOMAIN_TRUST_ACCOUNT', 2048),
                       ('WORKSTATION_TRUST_ACCOUNT', 4096), ('SERVER_TRUST_ACCOUNT', 8192),
                       ('DONT_EXPIRE_PASSWORD', 65536), ('MNS_LOGON_ACCOUNT', 131072),
                       ('SMARTCARD_REQUIRED', 262144), ('TRUSTED_FOR_DELEGATION', 524288),
                       ('NOT_DELEGATED', 1048576), ('USE_DES_KEY_ONLY', 2097152),
                       ('DONT_REQ_PREAUTH', 4194304), ('PASSWORD_EXPIRED', 8388608),
                       ('TRUSTED_TO_AUTH_FOR_DELEGATION', 16777216), ('NO_AUTH_DATA_REQUIRED', 33554432),
                       ('PARTIAL_SECRETS_ACCOUNT', 67108864))


syntax_registry.reg_at(UserAccountControl.oid, [
 '1.2.840.113556.1.4.8'])

class SystemFlags(BitArrayInteger):
    __doc__ = '\n    See\n    http://msdn.microsoft.com/library/default.asp?url=/library/en-us/adschema/adschema/a_systemflags.asp\n    and\n    http://msdn2.microsoft.com/en-us/library/aa772297.aspx\n    '
    oid = 'SystemFlags-oid'
    oid: str
    flag_desc_table = (('ADS_SYSTEMFLAG_DISALLOW_DELETE', 2147483648), ('ADS_SYSTEMFLAG_CONFIG_ALLOW_RENAME', 1073741824),
                       ('ADS_SYSTEMFLAG_CONFIG_ALLOW_MOVE', 536870912), ('ADS_SYSTEMFLAG_CONFIG_ALLOW_LIMITED_MOVE', 268435456),
                       ('ADS_SYSTEMFLAG_DOMAIN_DISALLOW_RENAME', 134217728), ('ADS_SYSTEMFLAG_DOMAIN_DISALLOW_MOVE', 67108864),
                       ('ADS_SYSTEMFLAG_CR_NTDS_NC', 1), ('ADS_SYSTEMFLAG_CR_NTDS_DOMAIN', 2),
                       ('ADS_SYSTEMFLAG_ATTR_NOT_REPLICATED', 1), ('ADS_SYSTEMFLAG_ATTR_IS_CONSTRUCTED', 4),
                       ('IS_CATEGORY_1_OBJECT', 16), ('IS_NOT_MOVED_TO_THE_DELETED_OBJECTS', 33554432))


syntax_registry.reg_at(SystemFlags.oid, [
 '1.2.840.113556.1.4.375'])

class SearchFlags(BitArrayInteger):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/ms679765(VS.85).aspx\n\n     1 (0x00000001)   Create an index for the attribute.\n     2 (0x00000002)   Create an index for the attribute in each container.\n     4 (0x00000004)   Add this attribute to the Ambiguous Name Resolution (ANR) set. This is used to assist in finding an object when only partial information is given. For example, if the LDAP filter is (ANR=JEFF), the search will find each object where the first name, last name, e-mail address, or other ANR attribute is equal to JEFF. Bit 0 must be set for this index take affect.\n     8 (0x00000008)   Preserve this attribute in the tombstone object for deleted objects.\n    16 (0x00000010)   Copy the value for this attribute when the object is copied.\n    32 (0x00000020)   Supported beginning with Windows Server 2003. Create a tuple index for the attribute. This will improve searches where the wildcard appears at the front of the search string. For example, (sn=*mith).\n    64 (0x00000040)   Supported beginning with ADAM. Creates an index to greatly help VLV performance on arbitrary attributes.\n    '
    oid = 'SearchFlags-oid'
    oid: str
    flag_desc_table = (('Indexed', 1), ('Indexed in each container', 2), ('Ambiguous Name Resolution (ANR)', 4),
                       ('Preserve in tombstone object', 8), ('Copy value when object copied', 16),
                       ('tuple index', 32), ('VLV index (Subtree Index in ADAM)', 64),
                       ('CONFIDENTIAL', 128), ('NEVER_AUDIT_VALUE', 256), ('RODC_FILTERED', 512),
                       ('', 1024), ('', 2048))


syntax_registry.reg_at(SearchFlags.oid, [
 '1.2.840.113556.1.2.334'])

class LogonHours(OctetString):
    oid = 'LogonHours-oid'
    oid: str
    desc = 'Logon hours'
    desc: str
    dayofweek = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')

    @staticmethod
    def _extract_hours(value):
        if not value or len(value) != 21:
            return []
        hour_flags = []
        for eight_hours in value:
            for i in range(8):
                hour_flags.append({0:'-',  1:'X'}[(eight_hours >> i & 1)])
            else:
                return hour_flags

    def sanitize(self, attrValue: bytes) -> bytes:
        if not attrValue:
            return b''
        attrValue = attrValue.replace(b'\r', b'').replace(b'\n', b'')
        hour_flags = [int(attrValue[i:i + 1] == b'X') << i % 8 for i in range(len(attrValue))]
        r = [sum(hour_flags[i * 8:(i + 1) * 8]) for i in range(21)]
        return bytes(r)

    def _validate(self, attrValue: bytes) -> bool:
        return len(attrValue) == 21

    def formValue(self) -> str:
        hour_flags = self._extract_hours(self._av)
        if hour_flags:
            day_bits = [''.join(hour_flags[24 * day:24 * day + 24]) for day in range(7)]
        else:
            day_bits = []
        return '\r\n'.join(day_bits)

    def formField(self) -> str:
        return web2ldap.web.forms.Textarea((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          1,
          None,
          default=(self.formValue()),
          rows=7,
          cols=24)

    def display(self, valueindex=0, commandbutton=False) -> str:
        hour_flags = self._extract_hours(self._av)
        result_lines = [
         '<tr>\n            <th width="10%%">Day</th>\n            <th colspan="3" width="8%%">0</th>\n            <th colspan="3" width="8%%">3</th>\n            <th colspan="3" width="8%%">6</th>\n            <th colspan="3" width="8%%">9</th>\n            <th colspan="3" width="8%%">12</th>\n            <th colspan="3" width="8%%">15</th>\n            <th colspan="3" width="8%%">18</th>\n            <th colspan="3" width="8%%">21</th>\n            </tr>']
        for day in range(7):
            day_bits = hour_flags[24 * day:24 * day + 24]
            result_lines.append('<tr><td>%s</td><td>%s</td></tr>' % (
             self.dayofweek[day],
             '</td><td>'.join(day_bits)))
        else:
            return '<p>%s</p><table>%s</table>' % (
             OctetString.display(self, valueindex, commandbutton),
             '\n'.join(result_lines))


syntax_registry.reg_at(LogonHours.oid, [
 '1.2.840.113556.1.4.64'])

class CountryCode(PropertiesSelectList):
    oid = 'CountryCode-oid'
    oid: str
    desc = 'Numerical country code'
    desc: str
    properties_pathname = os.path.join(web2ldapcnf.etc_dir, 'properties', 'attribute_select_countryCode.properties')
    simpleSanitizers = (
     bytes.strip,)

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        self.attr_value_dict['0'] = '-/-'
        SelectList.__init__(self, app, dn, schema, attrType, attrValue, entry)


syntax_registry.reg_at(CountryCode.oid, [
 '1.2.840.113556.1.4.25'])

class InstanceType(BitArrayInteger):
    __doc__ = '\n    http://msdn.microsoft.com/library/en-us/adschema/adschema/a_instancetype.asp\n    '
    oid = 'InstanceType-oid'
    oid: str
    flag_desc_table = (('The head of naming context.', 1), ('This replica is not instantiated.', 2),
                       ('The object is writable on this directory.', 4), ('The naming context above this one on this directory is held.', 8),
                       ('The naming context is in the process of being constructed for the first time via replication.', 16),
                       ('The naming context is in the process of being removed from the local DSA.', 32))


syntax_registry.reg_at(InstanceType.oid, [
 '1.2.840.113556.1.2.1'])

class DNWithOctetString(DistinguishedName):
    oid = '1.2.840.113556.1.4.903'
    oid: str
    desc = 'DNWithOctetString'
    desc: str
    octetTag = 'B'

    def _validate(self, attrValue: bytes) -> bool:
        try:
            octet_tag, count, octet_string, dn = self._app.ls.uc_decode(attrValue)[0].split(':')
        except ValueError:
            return False
        else:
            try:
                count = int(count)
            except ValueError:
                return False
            else:
                return len(octet_string) == count and octet_tag.upper() == self.octetTag and is_dn(dn)

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            octet_tag, count, octet_string, dn = self.av_u.split(':')
        except ValueError:
            return self._app.form.utf2display(self.av_u)
        else:
            return ':'.join([
             self._app.form.utf2display(octet_tag),
             self._app.form.utf2display(count),
             self._app.form.utf2display(octet_string),
             self._app.display_dn(dn,
               commandbutton=commandbutton)])


class DNWithString(DNWithOctetString):
    oid = '1.2.840.113556.1.4.904'
    oid: str
    desc = 'DNWithString'
    desc: str
    octetTag = 'S'


class MicrosoftLargeInteger(Integer):
    oid = '1.2.840.113556.1.4.906'
    oid: str
    desc = 'Integer guaranteed to support 64 bit numbers'
    desc: str


class ObjectSecurityDescriptor(OctetString):
    oid = '1.2.840.113556.1.4.907'
    oid: str
    desc = 'Object-Security-Descriptor'
    desc: str


class MsAdGUID(OctetString):
    oid = 'MsAdGUID-oid'
    oid: str
    desc = 'GUID in Active Directory'
    desc: str

    def sanitize(self, attrValue: bytes) -> bytes:
        try:
            object_guid_uuid = uuid.UUID(attrValue.decode('ascii').replace(':', ''))
        except ValueError:
            return OctetString.sanitize(self, attrValue)
        else:
            return object_guid_uuid.bytes

    def display(self, valueindex=0, commandbutton=False) -> str:
        object_guid_uuid = uuid.UUID(bytes=(self._av))
        return '{%s}<br>%s' % (
         str(object_guid_uuid),
         OctetString.display(self, valueindex=0, commandbutton=False))


syntax_registry.reg_at(MsAdGUID.oid, [
 '1.2.840.113556.1.4.2',
 '1.2.840.113556.1.4.1224',
 '1.2.840.113556.1.4.340',
 '1.2.840.113556.1.4.362'])

class Interval(MicrosoftLargeInteger):
    oid = 'Interval-oid'
    oid: str
    desc = 'Large integer with timestamp expressed as 100 nanoseconds since 1601-01-01 00:00'
    desc: str

    @staticmethod
    def _delta(attrValue):
        return (int(attrValue) - 116444736000000000) / 10000000

    def display(self, valueindex=0, commandbutton=False) -> str:
        if self.av_u == '9223372036854775807':
            return '-1: unlimited/off'
        delta = self._delta(self.av_u)
        if delta >= 0:
            return '%s (%s)' % (
             MicrosoftLargeInteger.display(self, valueindex, commandbutton),
             self._app.form.utf2display(str(strftimeiso8601(time.gmtime(delta)))))
        return self.av_u


class LockoutTime(Interval):
    oid = 'LockoutTime-oid'
    oid: str
    desc = 'Timestamp of password failure lockout'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        delta = self._delta(self._av)
        if delta == 0:
            return '%s (not locked)' % MicrosoftLargeInteger.display(self, valueindex, commandbutton)
        if delta < 0:
            return MicrosoftLargeInteger.display(self, valueindex, commandbutton)
        return '%s (locked since %s)' % (
         MicrosoftLargeInteger.display(self, valueindex, commandbutton),
         self._app.form.utf2display(str(strftimeiso8601(time.gmtime(delta)))))


syntax_registry.reg_at(LockoutTime.oid, [
 '1.2.840.113556.1.4.662'])

class DomainFunctionality(SelectList):
    oid = 'DomainFunctionality-oid'
    oid: str
    desc = 'Functional level of domain/forest'
    desc: str
    attr_value_dict = {'':'', 
     '0':'Windows 2000', 
     '1':'Windows 2003 Mixed', 
     '2':'Windows 2003', 
     '3':'Windows 2008', 
     '4':'Windows 2008R2', 
     '5':'Windows 2012'}


syntax_registry.reg_at(DomainFunctionality.oid, [
 'domainFunctionality',
 'forestFunctionality'])

class DomainControllerFunctionality(SelectList):
    oid = 'DomainControllerFunctionality-oid'
    oid: str
    desc = 'Functional level of domain controller'
    desc: str
    attr_value_dict = {'':'', 
     '0':'Windows 2000', 
     '2':'Windows 2003', 
     '3':'Windows 2008', 
     '4':'Windows 2008R2', 
     '5':'Windows 2012', 
     '6':'Windows 2012R2'}


syntax_registry.reg_at(DomainFunctionality.oid, [
 'domainControllerFunctionality'])
syntax_registry.reg_at(Interval.oid, [
 '1.2.840.113556.1.4.159',
 '1.2.840.113556.1.4.49',
 '1.2.840.113556.1.4.52',
 '1.2.840.113556.1.4.1696',
 '1.2.840.113556.1.4.51',
 '1.2.840.113556.1.4.96'])

class ServerStatus(SelectList):
    oid = 'ServerStatus-oid'
    oid: str
    desc = 'Specifies whether the server is enabled or disabled.'
    desc: str
    attr_value_dict = {'':'',  '1':'enabled', 
     '2':'disabled'}


syntax_registry.reg_at(ServerStatus.oid, [
 '1.2.840.113556.1.4.154'])

class ObjectClassCategory(SelectList):
    oid = 'ObjectClassCategory-oid'
    oid: str
    desc = 'Category for object class'
    desc: str
    attr_value_dict = {'1':'STRUCTURAL',  '2':'ABSTRACT', 
     '3':'AUXILIARY'}


syntax_registry.reg_at(ObjectClassCategory.oid, [
 '1.2.840.113556.1.2.370'])

class ClassSchemaLDAPName(DynamicValueSelectList, OID):
    oid = 'ClassSchema-oid'
    oid: str
    desc = 'lDAPDisplayName of the classSchema entry'
    desc: str
    ldap_url = 'ldap:///_?lDAPDisplayName,lDAPDisplayName?one?(objectClass=classSchema)'

    def display(self, valueindex=0, commandbutton=False) -> str:
        return OID.display(self, valueindex, commandbutton)


syntax_registry.reg_at(ClassSchemaLDAPName.oid, [
 '1.2.840.113556.1.2.351',
 '1.2.840.113556.1.4.198',
 '1.2.840.113556.1.2.8',
 '1.2.840.113556.1.4.195'])

class AttributeSchemaLDAPName(DynamicValueSelectList, OID):
    oid = 'AttributeSchema-oid'
    oid: str
    desc = 'lDAPDisplayName of the classSchema entry'
    desc: str
    ldap_url = 'ldap:///_?lDAPDisplayName,lDAPDisplayName?one?(objectClass=attributeSchema)'

    def display(self, valueindex=0, commandbutton=False) -> str:
        return OID.display(self, valueindex, commandbutton)


syntax_registry.reg_at(AttributeSchemaLDAPName.oid, [
 '1.2.840.113556.1.2.25',
 '1.2.840.113556.1.4.196',
 '1.2.840.113556.1.2.24',
 '1.2.840.113556.1.4.197'])

class PwdProperties(BitArrayInteger):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/ms679431(VS.85).aspx\n    '
    oid = 'PwdProperties-oid'
    oid: str
    flag_desc_table = (('DOMAIN_PASSWORD_COMPLEX', 1), ('DOMAIN_PASSWORD_NO_ANON_CHANGE', 2),
                       ('DOMAIN_PASSWORD_NO_CLEAR_CHANGE', 4), ('DOMAIN_LOCKOUT_ADMINS', 8),
                       ('DOMAIN_PASSWORD_STORE_CLEARTEXT', 16), ('DOMAIN_REFUSE_PASSWORD_CHANGE', 32))


syntax_registry.reg_at(PwdProperties.oid, [
 '1.2.840.113556.1.4.93'])

class MsDSSupportedEncryptionTypes(BitArrayInteger):
    oid = 'MsDSSupportedEncryptionTypes-oid'
    oid: str
    flag_desc_table = (('KERB_ENCTYPE_DES_CBC_CRC', 1), ('KERB_ENCTYPE_DES_CBC_MD5', 2),
                       ('KERB_ENCTYPE_RC4_HMAC_MD5', 4), ('KERB_ENCTYPE_AES128_CTS_HMAC_SHA1_96', 8),
                       ('KERB_ENCTYPE_AES256_CTS_HMAC_SHA1_96', 16))


syntax_registry.reg_at(MsDSSupportedEncryptionTypes.oid, [
 '1.2.840.113556.1.4.1963'])

class ShowInAddressBook(DynamicDNSelectList):
    oid = 'ShowInAddressBook-oid'
    oid: str
    desc = 'DN of the addressbook container entry'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=addressBookContainer)'


syntax_registry.reg_at(ShowInAddressBook.oid, [
 '1.2.840.113556.1.4.644'])

class MsDSReplAttributeMetaData(XmlValue):
    oid = 'MsDSReplAttributeMetaData-oid'
    oid: str
    editable = False
    editable: bool

    def _validate(self, attrValue: bytes) -> bool:
        return attrValue.endswith(b'\n\x00') and XmlValue._validate(self, attrValue[:-1])


syntax_registry.reg_at(MsDSReplAttributeMetaData.oid, [
 '1.2.840.113556.1.4.1707'])

class MsSFU30NisDomain(DynamicValueSelectList):
    oid = 'MsSFU30NisDomain-oid'
    oid: str
    desc = 'Name of NIS domain controlled by MS SFU'
    desc: str
    ldap_url = 'ldap:///_?cn,cn?sub?(objectClass=msSFU30DomainInfo)'


syntax_registry.reg_at(MsSFU30NisDomain.oid, [
 '1.2.840.113556.1.6.18.1.339'])
syntax_registry.reg_at((GroupEntryDN.oid),
  [
 '2.5.4.49'],
  structural_oc_oids=[
 '1.2.840.113556.1.5.8'])
syntax_registry.oid2syntax['Boolean'] = Boolean
syntax_registry.oid2syntax['DN'] = DistinguishedName
syntax_registry.oid2syntax['Integer'] = Integer
syntax_registry.oid2syntax['DirectoryString'] = DirectoryString
syntax_registry.oid2syntax['GeneralizedTime'] = GeneralizedTime
syntax_registry.reg_at(DistinguishedName.oid, [
 'configurationNamingContext',
 'defaultNamingContext',
 'dsServiceName',
 'rootDomainNamingContext',
 'schemaNamingContext',
 '1.2.840.113556.1.4.223'])
syntax_registry.reg_at(Binary.oid, [
 '1.2.840.113556.1.4.645',
 '1.2.840.113556.1.4.4',
 '1.2.840.113556.1.2.91',
 '1.2.840.113556.1.2.83',
 '1.2.840.113556.1.2.281'])
syntax_registry.reg_at(OctetString.oid, [
 '1.2.840.113556.1.4.138'])
syntax_registry.reg_at(Uri.oid, [
 '1.2.840.113556.1.4.583',
 '1.2.840.113556.1.2.464',
 '1.2.840.113556.1.4.749'])
syntax_registry.reg_at(DNSDomain.oid, [
 '1.2.840.113556.1.4.619'])
syntax_registry.reg_syntaxes(__name__)