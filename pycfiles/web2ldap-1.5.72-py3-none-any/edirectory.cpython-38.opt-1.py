# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/edirectory.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 14101 bytes
"""
web2ldap plugin classes for Novell eDirectory/DirXML
(see draft-sermersheim-nds-ldap-schema)
"""
import uuid
from binascii import hexlify
import ldap0.filter, web2ldapcnf
from web2ldap.app.schema.syntaxes import Binary, BitArrayInteger, DirectoryString, DynamicDNSelectList, Integer, MultilineText, NullTerminatedDirectoryString, OctetString, OID, PostalAddress, PreformattedMultilineText, PrintableString, SelectList, XmlValue, syntax_registry
from web2ldap.app.plugins.x509 import Certificate, CertificateList

class TaggedData(OctetString):
    oid = '2.16.840.1.113719.1.1.5.1.12'
    oid: str
    desc = 'Tagged Data'
    desc: str


class OctetList(OctetString):
    oid = '2.16.840.1.113719.1.1.5.1.13'
    oid: str
    desc = 'Octet List'
    desc: str


class TaggedString(DirectoryString):
    oid = '2.16.840.1.113719.1.1.5.1.14'
    oid: str
    desc = 'Tagged String'
    desc: str


class DollarSeparatedMultipleLines(PostalAddress):
    oid = '2.16.840.1.113719.1.1.5.1.6'
    oid: str
    desc = '$-separated string'
    desc: str


class OctetStringGUID(OctetString):
    oid = 'OctetStringGUID-oid'
    oid: str
    desc = 'GUID of eDirectory entries represented as 16 byte octet string'
    desc: str

    def _validate(self, attrValue: bytes) -> bool:
        return len(attrValue) == 16

    @staticmethod
    def _guid2association(s):
        """
        format association like Edir2Edir driver: {60445C8E-D8DB-d801-808C-0008028B1EF9}
        """
        s1 = hexlify(s).upper()
        return '{%s}' % '-'.join((
         ''.join((s1[6:8], s1[4:6], s1[2:4], s1[0:2])),
         ''.join((s1[10:12], s1[8:10])),
         ''.join((s1[14:16].lower(), s1[12:14].lower())),
         s1[16:20],
         s1[20:32]))

    @staticmethod
    def _guid2assoc(s):
        """
        format association like entitlement driver: {8E5C4460-DBD8-01D8-808C-0008028B1EF9}
        """
        s1 = hexlify(s).upper()
        return '{%s}' % '-'.join((
         s1[0:8],
         s1[8:12],
         s1[12:16],
         s1[16:20],
         s1[20:32]))

    @staticmethod
    def _guid2assoc_c1(s):
        """
        format association like C1 and iManager: 60445C8E-D8DB-d801-808C-0008028B1EF9
        """
        s1 = hexlify(s).upper()
        return ''.join((
         s1[6:8],
         s1[4:6],
         s1[2:4],
         s1[0:2],
         s1[10:12],
         s1[8:10],
         s1[14:16],
         s1[12:14],
         s1[16:32]))

    def display(self, valueindex=0, commandbutton=False) -> str:
        if self._at == 'GUID':
            return '\n            <table summary="GUID representation variants">\n              <tr><td>Octet String</td><td>%s</td></tr>\n              <tr><td>UUID</td><td>%s</td></tr>\n              <tr><td>Edir2Edir driver</td><td>%s</td></tr>\n              <tr><td>entitlement driver</td><td>%s</td></tr>\n              <tr><td>C1/iManager assoc.</td><td>%s</td></tr>\n            </table>\n            ' % (
             OctetString.display(self, valueindex, commandbutton),
             str(uuid.UUID(bytes=(self._av))),
             self._guid2association(self._av),
             self._guid2assoc(self._av),
             self._guid2assoc_c1(self._av))
        return web2ldapcnf.command_link_separator.join((
         self._guid2assoc_c1(self._av),
         self._app.anchor('searchform',
           '&raquo;', [
          (
           'dn', self._dn),
          (
           'filterstr', ldap0.filter.escape_str(self._av)),
          ('searchform_mode', 'exp')],
           title='Search entry with this GUID')))


syntax_registry.reg_at(OctetStringGUID.oid, [
 '2.16.840.1.113719.1.1.4.1.501',
 '2.16.840.1.113719.1.280.4.931.1',
 '2.16.840.1.113719.1.14.4.1.50',
 '2.16.840.1.113719.1.1.4.1.502'])

class IndexDefinition(DollarSeparatedMultipleLines):
    __doc__ = '\n    Version: 0 (reserved for future use)\n    Name: description of index\n    State: 0-suspend, 1-bringing, 2-online, 3-pending\n    Matching Rule: 0-value, 1-presence, 2-substring\n    Type: 0-user defined\n    Value State: 1-added from server\n    NDS Attribute Name\n    '
    oid = 'IndexDefinition-oid'
    oid: str
    desc = 'Index Definition'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            version, index_name, state, matching_rule, index_type, value_state, nds_attribute_name = self._av.split('$')
            version = int(version)
            index_name = self._app.ls.uc_decode(index_name)[0]
            state = int(state)
            matching_rule = int(matching_rule)
            index_type = int(index_type)
            value_state = int(value_state)
            nds_attribute_name = self._app.ls.uc_decode(nds_attribute_name)[0]
        except (ValueError, UnicodeDecodeError):
            return DollarSeparatedMultipleLines.display(self, valueindex, commandbutton)
        else:
            return '\n          <table>\n            <tr><td>Version:</td><td>%s</td></tr>\n            <tr><td>Name:</td><td>%s</td></tr>\n            <tr><td>State:</td><td>%s</td></tr>\n            <tr><td>Matching Rule:</td><td>%s</td></tr>\n            <tr><td>Type:</td><td>%s</td></tr>\n            <tr><td>Value State:</td><td>%s</td></tr>\n            <tr><td>NDS Attribute Name</td><td>%s</td></tr>\n          </table>' % (
             version,
             index_name.encode(self._app.form.accept_charset),
             {0:'suspend', 
              1:'bringing',  2:'online',  3:'pending'}.get(state, str(state)),
             {0:'value', 
              1:'presence',  2:'substring'}.get(matching_rule, str(matching_rule)),
             {0: 'user defined'}.get(index_type, str(index_type)),
             {1: 'added from server'}.get(value_state, str(value_state)),
             nds_attribute_name.encode(self._app.form.accept_charset))


syntax_registry.reg_at(IndexDefinition.oid, [
 '2.16.840.1.113719.1.1.4.1.512'])

class TaggedNameAndString(DirectoryString, OctetString):
    oid = '2.16.840.1.113719.1.1.5.1.15'
    oid: str
    desc = 'Tagged Name And String'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            ind2 = self._av.rindex('#')
            ind1 = self._av.rindex('#', 0, ind2 - 1)
        except ValueError:
            return DirectoryString.display(self, valueindex, commandbutton)
        else:
            dn = self._app.ls.uc_decode(self._av[0:ind1])[0]
            number = self._av[ind1 + 1:ind2]
            dstring = self._av[ind2 + 1:]
            try:
                dstring.decode('utf8')
            except UnicodeError:
                dstring_disp = OctetString.display(self, valueindex, commandbutton)
            else:
                dstring_disp = DirectoryString.display(self, valueindex, commandbutton)
            return '<dl><dt>name:</dt><dd>%s</dd><dt>number:</dt><dd>%s</dd><dt>dstring:</dt><dd><code>%s</code></dd></dl>' % (
             self._app.display_dn(dn, commandbutton=commandbutton),
             number,
             dstring_disp)


class NDSReplicaPointer(OctetString):
    oid = '2.16.840.1.113719.1.1.5.1.16'
    oid: str
    desc = 'NDS Replica Pointer'
    desc: str


class NDSACL(DirectoryString):
    oid = '2.16.840.1.113719.1.1.5.1.17'
    oid: str
    desc = 'NDS ACL'
    desc: str


class NDSTimestamp(PrintableString):
    oid = '2.16.840.1.113719.1.1.5.1.19'
    oid: str
    desc = 'NDS Timestamp'
    desc: str


class Counter(Integer):
    oid = '2.16.840.1.113719.1.1.5.1.22'
    oid: str
    desc = 'Counter (NDS)'
    desc: str


class TaggedName(DirectoryString):
    oid = '2.16.840.1.113719.1.1.5.1.23'
    oid: str
    desc = 'Tagged Name'
    desc: str


class TypedName(DirectoryString):
    oid = '2.16.840.1.113719.1.1.5.1.25'
    oid: str
    desc = 'Typed Name'
    desc: str


class EntryFlags(BitArrayInteger):
    __doc__ = '\n    See\n    '
    oid = 'EntryFlags-oid'
    oid: str
    flag_desc_table = (('DS_ALIAS_ENTRY', 1), ('DS_PARTITION_ROOT', 2), ('DS_CONTAINER_ENTRY', 4),
                       ('DS_CONTAINER_ALIAS', 8), ('DS_MATCHES_LIST_FILTER', 16),
                       ('DS_REFERENCE_ENTRY', 32), ('DS_40X_REFERENCE_ENTRY', 64),
                       ('DS_BACKLINKED', 128), ('DS_NEW_ENTRY', 256), ('DS_TEMPORARY_REFERENCE', 512),
                       ('DS_AUDITED', 1024), ('DS_ENTRY_NOT_PRESENT', 2048), ('DS_ENTRY_VERIFY_CTS', 4096),
                       ('DS_ENTRY_DAMAGED', 8192))


syntax_registry.reg_at(EntryFlags.oid, [
 '2.16.840.1.113719.1.27.4.48'])

class NspmConfigurationOptions(BitArrayInteger):
    __doc__ = '\n    See http://ldapwiki.willeke.com/wiki/UniversalPasswordSecretBits\n    '
    oid = 'NspmConfigurationOptions-oid'
    oid: str
    flag_desc_table = (('On set password request the NDS password hash will be removed by SPM', 1),
                       ('On set password request the NDS password hash will not be set by SPM', 2),
                       ('On set password request the Simple password will not be set by SPM', 4),
                       ('Reserved 0x08', 8), ('Allow password retrieval by self (User)', 16),
                       ('Allow password retrieval by admin', 32), ('Allow password retrieval by password agents (trusted app)', 64),
                       ('Reserved 0x80', 128), ('Password enabled', 256), ('Advanced password policy enabled', 512))


syntax_registry.reg_at(NspmConfigurationOptions.oid, [
 '2.16.840.1.113719.1.39.43.4.100'])

class SnmpTrapDescription(MultilineText):
    oid = 'SnmpTrapDescription-oid'
    oid: str
    desc = 'SNMP Trap Description'
    desc: str
    lineSep = b'\x00'
    cols = 30


syntax_registry.reg_at(SnmpTrapDescription.oid, [
 '2.16.840.1.113719.1.6.4.4'])

class SASVendorSupport(PreformattedMultilineText):
    oid = 'SASVendorSupport-oid'
    oid: str
    desc = 'SAS Vendor Support'
    desc: str
    cols = 50


syntax_registry.reg_at(SASVendorSupport.oid, [
 '2.16.840.1.113719.1.39.42.1.0.12'])

class NspmPasswordPolicyDN(DynamicDNSelectList):
    oid = 'NspmPasswordPolicyDN-oid'
    oid: str
    desc = 'DN of the nspmPasswordPolicy entry'
    desc: str
    ldap_url = 'ldap:///cn=Password Policies,cn=Security?cn?sub?(objectClass=nspmPasswordPolicy)'


syntax_registry.reg_at(NspmPasswordPolicyDN.oid, [
 '2.16.840.1.113719.1.39.43.4.6'])

class DirXMLDriverStartOption(SelectList):
    oid = 'DirXML-DriverStartOption-oid'
    oid: str
    desc = 'Start option for a DirXML driver'
    desc: str
    attr_value_dict = {'0':'disabled',  '1':'manual', 
     '2':'auto'}


syntax_registry.reg_at(DirXMLDriverStartOption.oid, [
 '2.16.840.1.113719.1.14.4.1.13'])

class DirXMLState(SelectList):
    oid = 'DirXML-State-DriverStartOption-oid'
    oid: str
    desc = 'Current state of a DirXML driver'
    desc: str
    attr_value_dict = {'0':'stopped',  '1':'starting', 
     '2':'running', 
     '3':'stopping'}


syntax_registry.reg_at(DirXMLState.oid, [
 '2.16.840.1.113719.1.14.4.1.14'])
syntax_registry.reg_at(Certificate.oid, [
 '2.16.840.1.113719.1.48.4.1.3'])
syntax_registry.reg_at(CertificateList.oid, [
 '2.16.840.1.113719.1.48.4.1.34'])
syntax_registry.reg_at(OID.oid, [
 'supportedGroupingTypes'])
syntax_registry.reg_at(NullTerminatedDirectoryString.oid, [
 '2.16.840.1.113719.1.27.4.42'])
syntax_registry.reg_at(Binary.oid, [
 '2.16.840.1.113719.1.48.4.1.4',
 '2.16.840.1.113719.1.48.4.1.2',
 '2.16.840.1.113719.1.48.4.1.1',
 '2.16.840.1.113719.1.14.4.1.42',
 '2.16.840.1.113719.1.200.4.1',
 '2.16.840.1.113719.1.200.4.2',
 '2.16.840.1.113719.1.200.4.3',
 '2.16.840.1.113719.1.1.4.1.84'])
syntax_registry.reg_at(XmlValue.oid, [
 '2.16.840.1.113719.1.1.4.1.295',
 '2.16.840.1.113719.1.14.4.1.3',
 '2.16.840.1.113719.1.14.4.1.8',
 '2.16.840.1.113719.1.14.4.1.11',
 '2.16.840.1.113719.1.14.4.1.24',
 '2.16.840.1.113719.1.14.4.1.29',
 '2.16.840.1.113719.1.14.4.1.54',
 '2.16.840.1.113719.1.14.4.1.56',
 '2.16.840.1.113719.1.14.4.1.58',
 '2.16.840.1.113719.1.14.4.1.82',
 '2.16.840.1.113719.1.39.44.4.1',
 '2.16.840.1.113719.1.39.44.4.2',
 '2.16.840.1.113719.1.39.44.4.7',
 '2.16.840.1.113719.1.347.4.1'])
syntax_registry.reg_syntaxes(__name__)