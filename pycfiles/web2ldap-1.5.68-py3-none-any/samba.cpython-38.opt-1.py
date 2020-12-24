# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/samba.py
# Compiled at: 2019-11-26 05:03:32
# Size of source mod 2**32: 7896 bytes
"""
web2ldap plugin classes for Samba 3
"""
import string, re, ldap0, ldap0.filter
from web2ldap.app.schema.syntaxes import DirectoryString, SelectList, SecondsSinceEpoch, IA5String, DynamicValueSelectList, syntax_registry
from web2ldap.app.plugins.activedirectory import LogonHours
syntax_registry.reg_at(SecondsSinceEpoch.oid, [
 '1.3.6.1.4.1.7165.2.1.3',
 '1.3.6.1.4.1.7165.2.1.5',
 '1.3.6.1.4.1.7165.2.1.6',
 '1.3.6.1.4.1.7165.2.1.7',
 '1.3.6.1.4.1.7165.2.1.8',
 '1.3.6.1.4.1.7165.2.1.9',
 '1.3.6.1.4.1.7165.2.1.27',
 '1.3.6.1.4.1.7165.2.1.28',
 '1.3.6.1.4.1.7165.2.1.29',
 '1.3.6.1.4.1.7165.2.1.30',
 '1.3.6.1.4.1.7165.2.1.31',
 '1.3.6.1.4.1.7165.2.1.32'])
syntax_registry.reg_at(LogonHours.oid, [
 '1.3.6.1.4.1.7165.2.1.55'])

class SambaAcctFlags(IA5String):
    oid = 'SambaAcctFlags-oid'
    oid: str
    desc = 'Samba 3 account flags'
    desc: str
    input_pattern = '^\\[[NDHTUMWSLXI ]{0,16}\\]$'
    input_pattern: str
    reObj = re.compile(input_pattern)
    flags_dict = {'N':'<b>N</b>o password.', 
     'D':'<b>D</b>isabled.', 
     'H':'<b>H</b>omedir required.', 
     'T':'<b>T</b>emp account.', 
     'U':'<b>U</b>ser account (normal)', 
     'M':'<b>M</b>NS logon user account.', 
     'W':'<b>W</b>orkstation account.', 
     'S':'<b>S</b>erver account.', 
     'L':'<b>L</b>ocked account.', 
     'X':'No <b>X</b>piry on password', 
     'I':'<b>I</b>nterdomain trust account.'}

    def display(self, valueindex=0, commandbutton=False) -> str:
        flags = self._av[1:-1]
        table_rows = ['<tr><td>%s</td><td>%s</td></tr>\n' % ({True:'*',  False:''}[(f in flags)], d) for f, d in self.flags_dict.items()]
        return '<pre>%s</pre><table>\n%s\n</table>\n' % (
         self._app.form.utf2display(self.av_u),
         ''.join(table_rows))


syntax_registry.reg_at(SambaAcctFlags.oid, [
 '1.3.6.1.4.1.7165.2.1.26',
 '1.3.6.1.4.1.7165.2.1.4'])

class SambaSID(IA5String):
    oid = 'SambaSID-oid'
    oid: str
    desc = 'Samba SID (SDDL syntax)'
    desc: str
    input_pattern = '^S(-[0-9]+)+$'
    input_pattern: str
    reObj = re.compile(input_pattern)

    def _search_domain_entry(self, domain_name):
        if domain_name:
            domain_filter = '(&(objectClass=sambaDomain)(sambaDomainName=%s))' % ldap0.filter.escape_str(domain_name)
        else:
            domain_filter = '(objectClass=sambaDomain)'
        try:
            ldap_result = self._app.ls.l.search_s((self._app.naming_context.encode(self._app.ls.charset)),
              (ldap0.SCOPE_SUBTREE),
              domain_filter,
              attrlist=[
             'sambaSID', 'sambaDomainName'],
              sizelimit=2)
        except ldap0.NO_SUCH_OBJECT:
            return
        else:
            if len(ldap_result) != 1:
                return
            try:
                _, domain_entry = ldap_result[0].entry_as
            except (KeyError, IndexError):
                return
            else:
                return domain_entry

    def _get_domain_sid(self):
        try:
            primary_group_sid = self._entry['sambaPrimaryGroupSID'][0]
        except (KeyError, IndexError):
            domain_name = self._entry.get('sambaDomainName', [None])[0]
            domain_entry = self._search_domain_entry(domain_name)
            if domain_entry is None:
                domain_sid = None
            else:
                domain_sid = domain_entry.get('sambaSID', [None])[0]
        else:
            domain_sid = primary_group_sid.rsplit('-', 1)[0]
        return domain_sid

    def formValue(self) -> str:
        ocs = self._entry.object_class_oid_set()
        result = IA5String.formValue(self)
        if result:
            return result
        domain_sid = self._get_domain_sid()
        if domain_sid is not None:
            try:
                if 'sambaSamAccount' in ocs and 'posixAccount' in ocs:
                    uid_number = int(self._entry['uidNumber'][0])
                    result = '-'.join((
                     self._get_domain_sid(),
                     str(2 * uid_number + 1000)))
                else:
                    if 'sambaGroupMapping' in ocs and 'posixGroup' in ocs:
                        gid_number = int(self._entry['gidNumber'][0])
                        result = '-'.join((
                         self._get_domain_sid(),
                         str(2 * gid_number + 1001)))
            except (IndexError, KeyError, ValueError):
                pass

        return result


syntax_registry.reg_at(SambaSID.oid, [
 '1.3.6.1.4.1.7165.2.1.20'])

class SambaForceLogoff(SelectList):
    oid = 'SambaForceLogoff-oid'
    oid: str
    desc = 'Disconnect Users outside logon hours (default: -1 => off, 0 => on)'
    desc: str
    attr_value_dict = {'':'',  '0':'on', 
     '-1':'off'}


syntax_registry.reg_at(SambaForceLogoff.oid, [
 '1.3.6.1.4.1.7165.2.1.66'])

class SambaLogonToChgPwd(SelectList):
    oid = 'SambaLogonToChgPwd-oid'
    oid: str
    desc = 'Force Users to logon for password change (default: 0 => off, 2 => on)'
    desc: str
    attr_value_dict = {'':'',  '0':'off', 
     '2':'on'}


syntax_registry.reg_at(SambaLogonToChgPwd.oid, [
 '1.3.6.1.4.1.7165.2.1.60'])

class SambaGroupType(SelectList):
    oid = 'SambaGroupType-oid'
    oid: str
    desc = 'Samba group type'
    desc: str
    attr_value_dict = {'':'',  '2':'Domain Group', 
     '4':'Local Group (Alias)', 
     '5':'Built-in Group (well-known)'}


syntax_registry.reg_at(SambaGroupType.oid, [
 '1.3.6.1.4.1.7165.2.1.19'])

class ReferencedSID(DynamicValueSelectList):
    oid = 'ReferencedSID-oid'
    oid: str
    desc = 'SID which points to another object'
    desc: str
    ldap_url = 'ldap:///_?sambaSID,cn?sub?'


syntax_registry.reg_at(ReferencedSID.oid, [
 '1.3.6.1.4.1.7165.2.1.51'])

class SambaGroupSID(DynamicValueSelectList):
    oid = 'SambaGroupSID-oid'
    oid: str
    desc = 'SID which points to Samba group object'
    desc: str
    ldap_url = 'ldap:///_?sambaSID,cn?sub?(objectClass=sambaGroupMapping)'


syntax_registry.reg_at(SambaGroupSID.oid, [
 '1.3.6.1.4.1.7165.2.1.23'])

class SambaDomainName(DynamicValueSelectList):
    oid = 'SambaDomainName-oid'
    oid: str
    desc = 'Name of Samba domain'
    desc: str
    ldap_url = 'ldap:///_?sambaDomainName,sambaDomainName?sub?(objectClass=sambaDomain)'


syntax_registry.reg_at(SambaDomainName.oid, [
 '1.3.6.1.4.1.7165.2.1.38'])
syntax_registry.reg_at((DirectoryString.oid),
  [
 '1.3.6.1.4.1.7165.2.1.38'],
  structural_oc_oids=[
 '1.3.6.1.4.1.7165.2.2.5'])

class SambaHomeDrive(SelectList):
    oid = 'SambaHomeDrive-oid'
    oid: str
    desc = 'Samba home drive letter'
    desc: str
    attr_value_dict = dict([(
     driveletter, driveletter) for driveletter in ['%s:' % letter for letter in string.ascii_lowercase.upper()]])


syntax_registry.reg_at(SambaHomeDrive.oid, [
 '1.3.6.1.4.1.7165.2.1.33'])
syntax_registry.reg_syntaxes(__name__)